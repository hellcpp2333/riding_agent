"""骑行水平与体能查询路由。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import FitnessHistoryPoint, FitnessMatchResponse, FitnessProfileResponse
from app.auth.dependencies import get_current_user
from app.db_mysql import async_session_factory
from app.models import ActivityRecord, FitnessProfile, User
from app.services.fitness_service import evaluate_route_difficulty

router = APIRouter(prefix="/api/fitness", tags=["fitness"])


@router.get("", response_model=FitnessProfileResponse)
async def get_fitness(
    user: User = Depends(get_current_user),
):
    async with async_session_factory() as session:
        stmt = select(FitnessProfile).where(FitnessProfile.user_id == user.id)
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()

    if not profile:
        return FitnessProfileResponse(
            ftp=None,
            ftp_wkg=None,
            ftp_confidence=0.0,
            fitness_level="beginner",
            has_power=False,
            updated_at=None,
        )

    return FitnessProfileResponse(
        ftp=profile.ftp,
        ftp_wkg=profile.ftp_wkg,
        ftp_confidence=profile.ftp_confidence,
        fitness_level=profile.fitness_level,
        has_power=profile.ftp is not None and profile.ftp > 0,
        updated_at=profile.updated_at,
    )


@router.get("/history", response_model=list[FitnessHistoryPoint])
async def get_fitness_history(
    user: User = Depends(get_current_user),
):
    """FTP 变化趋势：从每条活动记录的 power_curve 推导 FTP。"""
    from app.services.fit_service import compute_ftp_from_curve

    async with async_session_factory() as session:
        stmt = (
            select(ActivityRecord)
            .where(ActivityRecord.user_id == user.id)
            .order_by(ActivityRecord.start_time.asc())
        )
        result = await session.execute(stmt)
        records = result.scalars().all()

    history: list[FitnessHistoryPoint] = []
    for r in records:
        if r.power_curve and len(r.power_curve) > 0:
            ftp = compute_ftp_from_curve(r.power_curve)
            if ftp:
                history.append(FitnessHistoryPoint(
                    ftp=ftp,
                    ftp_wkg=None,
                    activity_date=r.start_time or r.created_at,
                    activity_name=r.name,
                ))

    return history


@router.post("/match-route/{route_id}", response_model=FitnessMatchResponse)
async def match_route(
    route_id: int,
    user: User = Depends(get_current_user),
):
    """评估特定路线与用户体能的匹配度。"""
    async with async_session_factory() as session:
        from app.models import Route
        stmt = select(Route).where(Route.id == route_id, Route.user_id == user.id)
        result = await session.execute(stmt)
        route = result.scalar_one_or_none()
        if not route:
            raise HTTPException(404, "路线不存在")

        profile_stmt = select(FitnessProfile).where(FitnessProfile.user_id == user.id)
        result = await session.execute(profile_stmt)
        profile = result.scalar_one_or_none()

    fitness = {
        "ftp": profile.ftp if profile else None,
        "ftp_wkg": profile.ftp_wkg if profile else None,
        "fitness_level": profile.fitness_level if profile else "beginner",
        "has_power": (profile is not None and profile.ftp is not None and profile.ftp > 0),
    }

    match = evaluate_route_difficulty(
        route_distance_m=route.distance,
        route_elevation_m=route.elevation_gain,
        estimated_time_s=route.distance / 5.0,  # 默认 5 m/s ≈ 18 km/h
        user_fitness=fitness,
    )
    return match
