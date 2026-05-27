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
