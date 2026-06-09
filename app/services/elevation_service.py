import json
import urllib.request

from app.services.route_service import haversine_distance

OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"


def lookup_elevations(points: list[dict]) -> list[dict]:
    """调用 open-elevation API 查询高程。
    points: [{"lat": x, "lon": y}, ...]
    返回: [{"lat": x, "lon": y, "ele": z}, ...]
    """
    locations = [{"latitude": p["lat"], "longitude": p["lon"]} for p in points]
    body = json.dumps({"locations": locations}).encode()
    req = urllib.request.Request(
        OPEN_ELEVATION_URL,
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    return [
        {"lat": r["latitude"], "lon": r["longitude"], "ele": r["elevation"]}
        for r in data["results"]
    ]


def sample_points(points: list[dict], interval_m: float = 500.0) -> list[dict]:
    """等距采样，减少 API 请求量。保留首尾点。"""
    if len(points) <= 2:
        return list(points)
    sampled = [points[0]]
    accumulated = 0.0
    for i in range(1, len(points)):
        d = haversine_distance(
            points[i - 1]["lat"], points[i - 1]["lon"],
            points[i]["lat"], points[i]["lon"],
        )
        accumulated += d
        if accumulated >= interval_m:
            sampled.append(points[i])
            accumulated = 0.0
    if sampled[-1] != points[-1]:
        sampled.append(points[-1])
    return sampled


def calculate_elevation_stats(points: list[dict]) -> dict:
    """计算爬升统计。points 需含 ele 字段。"""
    gain = 0.0
    loss = 0.0
    for i in range(1, len(points)):
        diff = points[i]["ele"] - points[i - 1]["ele"]
        if diff > 0:
            gain += diff
        else:
            loss += abs(diff)
    elevations = [p["ele"] for p in points]
    return {
        "elevation_gain": gain,
        "elevation_loss": loss,
        "max_elevation": max(elevations) if elevations else 0,
        "min_elevation": min(elevations) if elevations else 0,
        "point_count": len(points),
    }
