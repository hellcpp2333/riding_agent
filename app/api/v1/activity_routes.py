"""活动记录 CRUD 路由。"""

import json
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import ActivityDetailResponse, ActivityListItem, FitnessMatchResponse, TrackPoint
from app.auth.dependencies import get_current_user
import app.db_mysql as db_mysql
from app.models import ActivityRecord, FitnessProfile, User
from app.services.fit_service import compute_ride_summary, parse_fit
from app.services.fitness_service import estimate_ftp_from_activities, evaluate_route_difficulty
from app.services.route_service import upload_gpx_to_oss as upload_to_oss

router = APIRouter(prefix="/api/activities", tags=["activities"])

MAX_FIT_SIZE = 10 * 1024 * 1024  # 10MB


@router.get("", response_model=list[ActivityListItem])
async def list_activities(
    page: int = 1,
    page_size: int = 20,
    user: User = Depends(get_current_user),
):
    async with db_mysql.async_session_factory() as session:
        stmt = (
            select(ActivityRecord)
            .where(ActivityRecord.user_id == user.id)
            .order_by(ActivityRecord.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await session.execute(stmt)
        rows = result.scalars().all()
    return [ActivityListItem.model_validate(r) for r in rows]


@router.post("", response_model=ActivityListItem)
async def upload_activity(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    if not file.filename or not file.filename.lower().endswith(".fit"):
        raise HTTPException(400, "仅支持 .fit 文件格式")

    data = await file.read()
    if len(data) > MAX_FIT_SIZE:
        raise HTTPException(400, f"文件大小不能超过 {MAX_FIT_SIZE // 1024 // 1024}MB")

    # 解析 FIT
    try:
        fit_data = parse_fit(data)
    except ValueError as e:
        raise HTTPException(400, str(e))

    # 计算摘要
    summary = compute_ride_summary(fit_data["records"])

    # 上传原始 FIT 到 OSS
    ts = uuid.uuid4().hex[:8]
    ext = ".fit"
    safe_name = fit_data["name"].replace("/", "_").replace(" ", "_")[:64]
    fit_key = f"activities/{user.id}/{safe_name}_{ts}{ext}"
    fit_oss_url = upload_to_oss(data, fit_key, user.id)

    # 上传轨迹 JSON 到 OSS（如果数据量大）
    track_data = summary.pop("track_data", [])
    track_json = json.dumps(track_data, ensure_ascii=False).encode()
    track_oss_url = upload_to_oss(track_json, f"activities/{user.id}/{safe_name}_{ts}_track.json", user.id)

    # 保存活动记录
    async with db_mysql.async_session_factory() as session:
        record = ActivityRecord(
            user_id=user.id,
            name=fit_data["name"],
            fit_oss_url=fit_oss_url,
            distance=summary["distance"],
            duration=summary["duration"],
            elevation_gain=summary["elevation_gain"],
            avg_speed=summary["avg_speed"],
            avg_hr=summary["avg_hr"],
            avg_power=summary["avg_power"],
            avg_cadence=summary["avg_cadence"],
            max_hr=summary["max_hr"],
            max_power=summary["max_power"],
            np=summary["np"],
            tss=summary["tss"],
            if_score=summary["if_score"],
            power_curve=summary["power_curve"],
            hr_zones=summary["hr_zones"],
            track_data_oss_url=track_oss_url,
            device_info=fit_data["device_info"] or None,
            start_time=fit_data["start_time"],
            track_points=summary["track_points"],
        )
        session.add(record)
        await session.commit()
        await session.refresh(record)

    # 更新体能档案（异步，不阻塞上传响应）
    await _update_fitness(user.id)

    return ActivityListItem.model_validate(record)


@router.get("/{activity_id}", response_model=ActivityDetailResponse)
async def get_activity(
    activity_id: int,
    user: User = Depends(get_current_user),
):
    async with db_mysql.async_session_factory() as session:
        stmt = select(ActivityRecord).where(
            ActivityRecord.id == activity_id,
            ActivityRecord.user_id == user.id,
        )
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(404, "活动记录不存在")

    # 加载轨迹数据
    track_data = await _load_track_data(record.track_data_oss_url)

    # 加载体能匹配
    try:
        profile = await _get_fitness(user.id)
        fitness = {
            "ftp": profile.ftp if profile else None,
            "ftp_wkg": profile.ftp_wkg if profile else None,
            "fitness_level": profile.fitness_level if profile else "beginner",
            "has_power": True if (profile and profile.ftp) else False,
        }
        match = evaluate_route_difficulty(
            route_distance_m=record.distance,
            route_elevation_m=record.elevation_gain,
            estimated_time_s=record.duration,
            user_fitness=fitness,
        )
    except Exception:
        match = None

    return ActivityDetailResponse(
        id=record.id,
        name=record.name,
        distance=record.distance,
        duration=record.duration,
        elevation_gain=record.elevation_gain,
        avg_speed=record.avg_speed,
        avg_hr=record.avg_hr,
        avg_power=record.avg_power,
        avg_cadence=record.avg_cadence,
        max_hr=record.max_hr,
        max_power=record.max_power,
        np=record.np,
        tss=record.tss,
        if_score=record.if_score,
        power_curve=record.power_curve,
        hr_zones=record.hr_zones,
        device_info=record.device_info,
        start_time=record.start_time,
        track_points=record.track_points,
        created_at=record.created_at,
        track_data=[TrackPoint(lat=p["lat"], lon=p["lon"], ele=p.get("ele")) for p in track_data if p.get("lat") and p.get("lon")],
        fitness_match=match,
    )


@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int,
    user: User = Depends(get_current_user),
):
    from app.services.route_service import delete_gpx_from_oss as delete_oss

    async with db_mysql.async_session_factory() as session:
        stmt = select(ActivityRecord).where(
            ActivityRecord.id == activity_id,
            ActivityRecord.user_id == user.id,
        )
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()
        if not record:
            raise HTTPException(404, "活动记录不存在")

        # 删除 OSS 文件
        if record.fit_oss_url:
            delete_oss(record.fit_oss_url)
        if record.track_data_oss_url:
            delete_oss(record.track_data_oss_url)

        await session.delete(record)
        await session.commit()

    return {"ok": True}


# ── 内部辅助 ──────────────────────────────────────────────

async def _update_fitness(user_id: int):
    """上传活动后更新用户体能档案。"""
    from app.services.fit_service import compute_ftp_from_curve, merge_power_curves

    async with db_mysql.async_session_factory() as session:
        stmt = (
            select(ActivityRecord)
            .where(ActivityRecord.user_id == user_id)
            .order_by(ActivityRecord.created_at.desc())
            .limit(5)
        )
        result = await session.execute(stmt)
        activities = result.scalars().all()

    acts = []
    for a in activities:
        acts.append({
            "avg_speed": a.avg_speed,
            "distance": a.distance,
            "duration": a.duration,
            "elevation_gain": a.elevation_gain,
            "power_curve": a.power_curve,
        })

    fitness = estimate_ftp_from_activities(acts)

    async with db_mysql.async_session_factory() as session:
        stmt = select(FitnessProfile).where(FitnessProfile.user_id == user_id)
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()

        if profile:
            profile.ftp = fitness["ftp"]
            profile.ftp_wkg = fitness["ftp_wkg"]
            profile.ftp_confidence = fitness["ftp_confidence"]
            profile.fitness_level = fitness["fitness_level"]
        else:
            profile = FitnessProfile(
                user_id=user_id,
                ftp=fitness["ftp"],
                ftp_wkg=fitness["ftp_wkg"],
                ftp_confidence=fitness["ftp_confidence"],
                fitness_level=fitness["fitness_level"],
            )
            session.add(profile)
        await session.commit()


async def _get_fitness(user_id: int) -> FitnessProfile | None:
    async with db_mysql.async_session_factory() as session:
        stmt = select(FitnessProfile).where(FitnessProfile.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def _load_track_data(oss_url: str | None) -> list[dict]:
    """从 OSS 加载轨迹点 JSON。"""
    if not oss_url:
        return []
    try:
        from app.services.route_service import download_gpx_from_oss
        raw = download_gpx_from_oss(oss_url)
        return json.loads(raw)
    except Exception:
        return []
