import json
import math as _math
import re as _re
import urllib.request

from app.services.route_service import haversine_distance

OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"

# WGS-84 / GCJ-02 转换常量
_A = 6378245.0
_EE = 0.00669342162296594323


def _transform_lat(lng: float, lat: float) -> float:
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * _math.sqrt(abs(lng))
    ret += (20.0 * _math.sin(6.0 * lng * _math.pi) + 20.0 * _math.sin(2.0 * lng * _math.pi)) * 2.0 / 3.0
    ret += (20.0 * _math.sin(lat * _math.pi) + 40.0 * _math.sin(lat / 3.0 * _math.pi)) * 2.0 / 3.0
    ret += (160.0 * _math.sin(lat / 12.0 * _math.pi) + 320 * _math.sin(lat * _math.pi / 30.0)) * 2.0 / 3.0
    return ret


def _transform_lng(lng: float, lat: float) -> float:
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * _math.sqrt(abs(lng))
    ret += (20.0 * _math.sin(6.0 * lng * _math.pi) + 20.0 * _math.sin(2.0 * lng * _math.pi)) * 2.0 / 3.0
    ret += (20.0 * _math.sin(lng * _math.pi) + 40.0 * _math.sin(lng / 3.0 * _math.pi)) * 2.0 / 3.0
    ret += (150.0 * _math.sin(lng / 12.0 * _math.pi) + 300.0 * _math.sin(lng / 30.0 * _math.pi)) * 2.0 / 3.0
    return ret


def _wgs84_to_gcj02(lng: float, lat: float) -> tuple[float, float]:
    d_lat = _transform_lat(lng - 105.0, lat - 35.0)
    d_lng = _transform_lng(lng - 105.0, lat - 35.0)
    rad_lat = lat / 180.0 * _math.pi
    magic = 1 - _EE * _math.sin(rad_lat) ** 2
    sqrt_magic = _math.sqrt(magic)
    d_lat = (d_lat * 180.0) / ((_A * (1 - _EE)) / (magic * sqrt_magic) * _math.pi)
    d_lng = (d_lng * 180.0) / (_A / sqrt_magic * _math.cos(rad_lat) * _math.pi)
    return lng + d_lng, lat + d_lat


def _gcj02_to_wgs84(lng: float, lat: float) -> tuple[float, float]:
    wgs_lng, wgs_lat = lng, lat
    for _ in range(10):
        tmp_lng, tmp_lat = _wgs84_to_gcj02(wgs_lng, wgs_lat)
        d_lng = tmp_lng - lng
        d_lat = tmp_lat - lat
        if abs(d_lng) < 1e-7 and abs(d_lat) < 1e-7:
            break
        wgs_lng -= d_lng
        wgs_lat -= d_lat
    return wgs_lng, wgs_lat


def bd09_to_wgs84(lng: float, lat: float) -> tuple[float, float]:
    """百度坐标系 (BD-09) → WGS-84 坐标转换。"""
    # BD-09 → GCJ-02
    x = lng - 0.0065
    y = lat - 0.006
    z = _math.sqrt(x * x + y * y) - 0.00002 * _math.sin(y * _math.pi * 3000.0 / 180.0)
    theta = _math.atan2(y, x) - 0.000003 * _math.cos(x * _math.pi * 3000.0 / 180.0)
    gcj_lng = z * _math.cos(theta)
    gcj_lat = z * _math.sin(theta)
    # GCJ-02 → WGS-84
    return _gcj02_to_wgs84(gcj_lng, gcj_lat)


def convert_points_bd09_to_wgs84(points: list[dict]) -> list[dict]:
    """将坐标点列表从 BD-09 转换为 WGS-84。"""
    result = []
    for p in points:
        wgs_lng, wgs_lat = bd09_to_wgs84(p["lon"], p["lat"])
        result.append({"lat": wgs_lat, "lon": wgs_lng})
    return result


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


def smooth_elevations(points: list[dict], window: int = 5) -> list[dict]:
    """移动平均平滑高程，消除 GPS/DEM 噪声突跳。窗口越大越平滑。"""
    if len(points) < window:
        return list(points)
    half = window // 2
    result = []
    for i in range(len(points)):
        start = max(0, i - half)
        end = min(len(points), i + half + 1)
        avg = sum(points[j]["ele"] for j in range(start, end)) / (end - start)
        result.append({**points[i], "ele": avg})
    return result


def calculate_elevation_stats(points: list[dict], min_gain_threshold: float = 5.0) -> dict:
    """计算爬升统计。先平滑去噪，再累加正高差。points 需含 ele 字段。"""
    smoothed = smooth_elevations(points)
    gain = 0.0
    loss = 0.0
    for i in range(1, len(smoothed)):
        diff = smoothed[i]["ele"] - smoothed[i - 1]["ele"]
        if diff > min_gain_threshold:
            gain += diff
        elif diff < -min_gain_threshold:
            loss += abs(diff)
    elevations = [p["ele"] for p in smoothed]
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
