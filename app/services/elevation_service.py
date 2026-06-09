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

    Baidu MCP 返回的路线数据中，坐标可能以多种格式出现：
    1. 分号分隔的坐标串: "lng,lat;lng,lat;..."
    2. JSON path/polyline 字段
    3. 文本中的 (lat, lng) 或 (lng, lat) 数字对
    """
    points: list[dict] = []
    seen: set[tuple[float, float]] = set()

    def _add(a: float, b: float):
        p = _parse_coord_pair(a, b)
        if p is None:
            return
        key = (round(p["lat"], 6), round(p["lon"], 6))
        if key not in seen:
            seen.add(key)
            points.append(p)

    # 1. 找分号分隔的坐标串（Baidu 路线数据最常见格式）
    coord_blocks = _re.findall(
        r'((?:[\d.]+,[\d.]+;)+[\d.]+,[\d.]+)', text
    )
    for block in coord_blocks:
        for pair in block.split(";"):
            pair = pair.strip()
            if not pair:
                continue
            parts = pair.split(",")
            if len(parts) == 2:
                try:
                    _add(float(parts[0].strip()), float(parts[1].strip()))
                except ValueError:
                    continue

    # 2. JSON path/polyline 字段（含单个坐标对）
    for key in ("path", "polyline", "points"):
        paths = _re.findall(rf'"{key}"\s*:\s*"([^"]+)"', text)
        for path in paths:
            for pair in path.split(";"):
                pair = pair.strip()
                if not pair:
                    continue
                parts = pair.split(",")
                if len(parts) == 2:
                    try:
                        _add(float(parts[0].strip()), float(parts[1].strip()))
                    except ValueError:
                        continue

    # 3. 兜底：匹配文本中的 (number, number) 对
    if not points:
        pairs = _re.findall(
            r'\(?(-?\d{1,3}\.\d+),\s*(-?\d{1,3}\.\d+)\)?', text
        )
        for a_str, b_str in pairs:
            _add(float(a_str), float(b_str))

    return points


def _parse_coord_pair(a: float, b: float) -> dict | None:
    """判断 (a, b) 是 (lat, lon) 还是 (lon, lat)，返回 {"lat": ..., "lon": ...}。

    Baidu 坐标系下中国范围: lat 18~54, lon 73~135。
    a 和 b 谁在这个范围里决定谁是 lat/lon。
    """
    a_is_lat = 18 <= a <= 54
    b_is_lat = 18 <= b <= 54
    a_is_lon = 73 <= a <= 135
    b_is_lon = 73 <= b <= 135

    if a_is_lat and b_is_lon:
        return {"lat": a, "lon": b}
    elif b_is_lat and a_is_lon:
        return {"lat": b, "lon": a}
    # 如果都在合理范围，默认 a=lat, b=lon
    elif a_is_lat and b_is_lat:
        return {"lat": a, "lon": b}
    # 如果都不在合理范围，仍尝试返回
    elif -90 <= a <= 90 and -180 <= b <= 180:
        return {"lat": a, "lon": b}
    elif -90 <= b <= 90 and -180 <= a <= 180:
        return {"lat": b, "lon": a}
    return None
