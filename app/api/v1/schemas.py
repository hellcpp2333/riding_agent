from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None
    preferences: dict | None = None


class RoutePlanRequest(BaseModel):
    origin: str
    destination: str
    waypoints: list[str] | None = None
    avoid_highway: bool = False
    prefer_greenway: bool = True
    thread_id: str | None = None


class RouteImportResponse(BaseModel):
    id: int
    name: str
    distance: float
    elevation_gain: float
    track_points: int


class RouteListItem(BaseModel):
    id: int
    name: str
    distance: float
    source: str
    created_at: datetime

    class Config:
        from_attributes = True


class TrackPoint(BaseModel):
    lat: float
    lon: float
    ele: float | None = None


class RouteDetailResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    distance: float
    elevation_gain: float
    track_points: int
    source: str
    created_at: datetime
    track_data: list[TrackPoint]

    class Config:
        from_attributes = True


class RouteExportPlanRequest(BaseModel):
    name: str
    coordinates: list[TrackPoint]
