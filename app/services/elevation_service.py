import json
import re as _re
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


def extract_coordinates(text: str) -> list[dict]:
    """从 map_directions 返回的文本中提取坐标列表。
    支持两种格式：
    1. JSON 中的 path 字段（Baidu MCP 常见格式）: "lng,lat;lng,lat;..."
    2. 文本中的 lat/lon 数字对
    """
    points: list[dict] = []

    # 尝试从 JSON 中提取 path 字符串
    paths = _re.findall(r'"path"\s*:\s*"([^"]+)"', text)
    if paths:
        for path in paths:
            for pair in path.split(";"):
                pair = pair.strip()
                if not pair:
                    continue
                parts = pair.split(",")
                if len(parts) == 2:
                    try:
                        lon = float(parts[0].strip())
                        lat = float(parts[1].strip())
                        points.append({"lat": lat, "lon": lon})
                    except ValueError:
                        continue

    # 如果没找到 path，尝试匹配文本中的 lat/lon 数字对
    if not points:
        pairs = _re.findall(
            r'\(?(\d{1,2}\.\d{4,}),\s*(\d{2,3}\.\d{4,})\)?', text
        )
        for lat_str, lon_str in pairs:
            lat = float(lat_str)
            lon = float(lon_str)
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                points.append({"lat": lat, "lon": lon})

    return points
