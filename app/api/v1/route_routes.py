from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from urllib.parse import quote
import io

from app.api.v1.schemas import (
    RouteDetailResponse,
    RouteExportPlanRequest,
    RouteImportResponse,
    RouteListItem,
    TrackPoint,
)
from app.auth.dependencies import get_current_user
import app.db_mysql as db_mysql
from app.models import Route, User
from app.services.route_service import (
    delete_gpx_from_oss,
    download_gpx_from_oss,
    generate_gpx,
    MAX_GPX_SIZE,
    parse_gpx,
    upload_gpx_to_oss,
)

def _make_content_disposition(name: str) -> str:
    """生成安全的 Content-Disposition header，处理非 ASCII 字符"""
    safe_name = name.replace('"', '').replace("'", "")
    encoded = quote(f"{safe_name}.gpx")
    return f'attachment; filename*=UTF-8\'\'{encoded}'


router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.get("")
async def list_routes(user: User = Depends(get_current_user)):
    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        result = await db.execute(
            select(Route)
            .where(Route.user_id == user.id)
            .order_by(Route.created_at.desc())
        )
        routes = result.scalars().all()
        return {
            "routes": [
                RouteListItem(
                    id=r.id,
                    name=r.name,
                    distance=r.distance,
                    source=r.source,
                    created_at=r.created_at.isoformat() if r.created_at else "",
                )
                for r in routes
            ]
        }


@router.get("/{route_id}", response_model=RouteDetailResponse)
async def get_route(route_id: int, user: User = Depends(get_current_user)):
    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        result = await db.execute(
            select(Route).where(Route.id == route_id)
        )
        route = result.scalar_one_or_none()
        if route is None:
            raise HTTPException(status_code=404, detail="路书不存在")
        if route.user_id != user.id:
            raise HTTPException(status_code=403, detail="无权访问")

        gpx_data = download_gpx_from_oss(route.gpx_oss_url)
        _, track_points, _, _ = parse_gpx(gpx_data)

        return RouteDetailResponse(
            id=route.id,
            name=route.name,
            description=route.description,
            distance=route.distance,
            elevation_gain=route.elevation_gain,
            track_points=route.track_points,
            source=route.source,
            created_at=route.created_at.isoformat() if route.created_at else "",
            track_data=[TrackPoint(lat=p["lat"], lon=p["lon"], ele=p.get("ele")) for p in track_points],
        )


@router.post("/import", status_code=201)
async def import_gpx(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    if not file.filename or not file.filename.lower().endswith(".gpx"):
        raise HTTPException(status_code=400, detail="仅支持 .gpx 格式")

    file_data = await file.read()
    if len(file_data) > MAX_GPX_SIZE:
        raise HTTPException(status_code=400, detail="文件大小不能超过 10MB")

    name, points, distance, elevation_gain = parse_gpx(file_data)
    if not points:
        raise HTTPException(status_code=400, detail="GPX 格式无效：未找到轨迹点")

    oss_url = upload_gpx_to_oss(file_data, file.filename, user.id)

    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        route = Route(
            user_id=user.id,
            name=name,
            gpx_oss_url=oss_url,
            distance=distance,
            elevation_gain=elevation_gain,
            track_points=len(points),
            source="import",
        )
        db.add(route)
        await db.commit()
        await db.refresh(route)

        return RouteImportResponse(
            id=route.id,
            name=route.name,
            distance=route.distance,
            elevation_gain=route.elevation_gain,
            track_points=route.track_points,
        )


@router.get("/{route_id}/export")
async def export_gpx(route_id: int, user: User = Depends(get_current_user)):
    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        result = await db.execute(select(Route).where(Route.id == route_id))
        route = result.scalar_one_or_none()
        if route is None:
            raise HTTPException(status_code=404, detail="路书不存在")
        if route.user_id != user.id:
            raise HTTPException(status_code=403, detail="无权访问")

        gpx_data = download_gpx_from_oss(route.gpx_oss_url)
        return StreamingResponse(
            io.BytesIO(gpx_data),
            media_type="application/gpx+xml",
            headers={
                "Content-Disposition": _make_content_disposition(route.name),
            },
        )


@router.delete("/{route_id}", status_code=204)
async def delete_route(route_id: int, user: User = Depends(get_current_user)):
    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        result = await db.execute(select(Route).where(Route.id == route_id))
        route = result.scalar_one_or_none()
        if route is None:
            raise HTTPException(status_code=404, detail="路书不存在")
        if route.user_id != user.id:
            raise HTTPException(status_code=403, detail="无权访问")

        delete_gpx_from_oss(route.gpx_oss_url)
        await db.delete(route)
        await db.commit()


@router.post("/export-plan")
async def export_plan(
    req: RouteExportPlanRequest, user: User = Depends(get_current_user)
):
    gpx_xml = generate_gpx(req.name, req.coordinates)
    return StreamingResponse(
        io.BytesIO(gpx_xml.encode("utf-8")),
        media_type="application/gpx+xml",
        headers={
            "Content-Disposition": _make_content_disposition(req.name),
        },
    )
