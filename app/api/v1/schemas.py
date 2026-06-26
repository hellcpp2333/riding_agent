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


class FitnessMatchResponse(BaseModel):
    fit_level: str
    estimated_completion: float
    ftp_required: float | None = None
    your_ftp: float | None = None
    key_challenges: list[str] = []


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
    elevation: dict | None = None
    fitness_match: FitnessMatchResponse | None = None

    class Config:
        from_attributes = True


class RouteExportPlanRequest(BaseModel):
    name: str
    coordinates: list[TrackPoint]


# ── Activity schemas ─────────────────────────────────────

class ActivityListItem(BaseModel):
    id: int
    name: str
    distance: float
    duration: float
    elevation_gain: float
    avg_speed: float | None = None
    avg_hr: float | None = None
    avg_power: float | None = None
    tss: float | None = None
    start_time: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class PowerSegment(BaseModel):
    start_idx: int
    end_idx: int
    zone: int
    avg_power: float


class PowerProfilePoint(BaseModel):
    time_sec: float
    dist_km: float
    power: int | None = None
    hr: int | None = None
    speed: float | None = None
    cadence: int | None = None
    altitude: float | None = None


class ActivityDetailResponse(BaseModel):
    id: int
    name: str
    distance: float
    duration: float
    elevation_gain: float
    avg_speed: float | None = None
    avg_hr: float | None = None
    avg_power: float | None = None
    avg_cadence: float | None = None
    max_hr: int | None = None
    max_power: int | None = None
    np: float | None = None
    tss: float | None = None
    if_score: float | None = None
    power_curve: dict | None = None
    hr_zones: dict | None = None
    device_info: str | None = None
    start_time: datetime | None = None
    track_points: int
    created_at: datetime
    track_data: list[TrackPoint] = []
    power_segments: list[PowerSegment] | None = None
    power_profile: list[PowerProfilePoint] | None = None
    fitness_match: dict | None = None

    class Config:
        from_attributes = True


# ── Fitness schemas ──────────────────────────────────────

class FitnessProfileResponse(BaseModel):
    ftp: float | None = None
    ftp_wkg: float | None = None
    ftp_confidence: float = 0.0
    fitness_level: str = "beginner"
    has_power: bool = False
    updated_at: datetime | None = None


class FitnessHistoryPoint(BaseModel):
    ftp: float | None = None
    ftp_wkg: float | None = None
    activity_date: datetime
    activity_name: str
