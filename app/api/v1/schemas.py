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
    name: str
    distance: float
    elevation_gain: float
    track_points: int


class RouteListItem(BaseModel):
    id: int
    name: str
    distance: float
    source: str
    created_at: str


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
    created_at: str
    track_data: list[TrackPoint]


class RouteExportPlanRequest(BaseModel):
    name: str
    coordinates: list[TrackPoint]
