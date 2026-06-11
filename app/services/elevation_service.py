import json
import math as _math
import os as _os
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


def lookup_elevations_batched(points: list[dict], batch_size: int = 800) -> list[dict]:
    """分批查询高程，支持长路线（>1000点）。每批最多 batch_size 个点，单批失败重试一次。"""
    if len(points) <= batch_size:
        return lookup_elevations(points)

    results = []
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        # 确保相邻批次之间有一个重叠点，防止边界不连续
        if i > 0 and len(results) > 0:
            batch = [results[-1]] + batch
        for attempt in range(2):
            try:
                batch_result = lookup_elevations(batch)
                # 去重：移除可能重复的第一个点
                if i > 0 and len(results) > 0 and len(batch_result) > 0:
                    batch_result = batch_result[1:]
                results.extend(batch_result)
                break
            except Exception:
                if attempt == 1:
                    raise
    return results


def lookup_elevations_local(points: list[dict]) -> list[dict]:
    """高程查询——本地 SRTM DEM 优先，自动 fallback 到 Open Elevation API。
    与 lookup_elevations_batched 接口一致，直接替换即可。
    """
    try:
        from app.services.dem_service import lookup_elevations_local as _dem_lookup
        return _dem_lookup(points)
    except Exception:
        return lookup_elevations_batched(points)


def detect_climbs(points: list[dict], min_length: float = 1000.0,
                  min_start_grade: float = 3.0, stop_grade: float = 2.0) -> list[dict]:
    """从高程数据中检测爬坡段。参照 Garmin 算法：
    使用 5 点滑动窗口计算局部坡度，当坡度 >= min_start_grade 时标记为坡段起点，
    当坡度 < stop_grade 且已超过 min_length 和 200m 安全距离时结束坡段。
    返回爬坡段列表，含 startIdx, endIdx, avgGrade, distance, elevationGain, difficulty, difficultyLabel。
    """
    if not points or len(points) < 5:
        return []

    segments = []
    window = 5
    half = window // 2
    i = half  # 从第 2 个点开始（窗口前半部分）
    n = len(points)

    while i < n - half:
        # 5 点窗口局部坡度
        d_h = points[i + half]["ele"] - points[i - half]["ele"]
        d_d = points[i + half]["dist"] - points[i - half]["dist"]
        if d_d <= 0:
            i += 1
            continue
        grade = (d_h / d_d) * 100.0

        if grade >= min_start_grade:
            start = i
            end = i
            total_dh = 0.0
            # 向前扩展爬坡段
            while end < n - 1:
                end += 1
                seg_dh = points[end]["ele"] - points[end - 1]["ele"]
                if seg_dh > 0:
                    total_dh += seg_dh
                seg_dd = points[end]["dist"] - points[end - 1]["dist"]
                if seg_dd > 0:
                    seg_grade = (seg_dh / seg_dd) * 100.0
                    # 坡度持续低于停止线且已超过最小长度+200m 安全距离 → 坡段结束
                    if seg_grade < stop_grade and (points[end]["dist"] - points[start]["dist"]) > (min_length + 200):
                        end -= 1
                        break

            seg_dist = points[end]["dist"] - points[start]["dist"]
            if seg_dist >= min_length and total_dh > 0:
                avg_grade = total_dh / seg_dist * 100.0
                diff = classify_climb(avg_grade, seg_dist)
                if diff["level"] == 0:
                    i = end + 1
                    continue  # 未达到 UCI 评级标准，跳过
                segments.append({
                    "startIdx": start,
                    "endIdx": end,
                    "avgGrade": round(avg_grade, 1),
                    "distance": round(seg_dist, 1),
                    "elevationGain": round(total_dh, 1),
                    "difficulty": diff["level"],
                    "difficultyLabel": diff["label"],
                })
            i = end + 1
        else:
            i += 1

    return segments


def classify_climb(avg_grade: float, distance_m: float) -> dict:
    """UCI 标准 5 级爬坡分类。
    准入条件：长度 ≥ 1000m 且 平均坡度 ≥ 1.3%。
    评分公式：UCI Score = 长度(km) × 平均坡度(%)² 。
    阈值校准来源：refer/uci爬坡段分级规则.md

    | 等级 | 标签  | UCI Score 范围 | 示例                        |
    |------|-------|---------------|-----------------------------|
    | 1    | 4级   | 20 – 59       | 2km@5% = 50, 5km@2.5% = 31 |
    | 2    | 3级   | 60 – 159      | 1.6km@10% = 160             |
    | 3    | 2级   | 160 – 329     | 5km@8% = 320, 15km@4% = 240 |
    | 4    | 1级   | 330 – 600     | 8km@8% = 512, 20km@5% = 500 |
    | 5    | HC级  | > 600         | 10km@8% = 640               |
    """
    # UCI qualification: min 1000m, min 1.3% grade
    if distance_m < 1000 or avg_grade < 1.3:
        return {"level": 0, "label": "未评级"}

    length_km = distance_m / 1000.0
    score = length_km * (avg_grade ** 2)

    if score > 600:
        return {"level": 5, "label": "HC级"}
    if score >= 400:
        return {"level": 4, "label": "1级"}
    if score >= 200:
        return {"level": 3, "label": "2级"}
    if score >= 80:
        return {"level": 2, "label": "3级"}
    if score >= 20:
        return {"level": 1, "label": "4级"}
    return {"level": 0, "label": "未评级"}


def enrich_route_with_elevation(track_points: list[dict], *, is_wgs84: bool = True) -> dict:
    """为路书轨迹点富化高程数据。
    若 track_points 中已有 ele 字段且不全为 0 → 直接使用并平滑计算。
    若无高程 → 采样后调用 Open Elevation API 补充。
    is_wgs84: GPX 导入的路书坐标已经是 WGS-84，无需 BD-09 转换。
    返回 {"points": [...], "stats": {...}, "climbs": [...]}
    """
    if not track_points:
        return {"points": [], "stats": {"gain": 0, "loss": 0, "max": 0, "min": 0}, "climbs": []}

    has_ele = any(p.get("ele", 0) != 0 for p in track_points)

    if has_ele:
        # GPX 文件自带高程（设备气压计/GPS），直接使用，不平滑
        points = calculate_cumulative_distances(track_points)
        points = smooth_elevations(points, window=1)
    else:
        # 无高程，调用 API 补充
        sampled = sample_points(track_points)
        if is_wgs84:
            elev = lookup_elevations_local(sampled)
            elev_with_dist = calculate_cumulative_distances(elev)
        else:
            wgs84_points = convert_points_bd09_to_wgs84(sampled)
            elev = lookup_elevations_local(wgs84_points)
            elev_with_dist = calculate_cumulative_distances(elev)
        points = savitzky_golay_smooth(elev_with_dist)

    stats = calculate_elevation_stats(points)
    climbs = detect_climbs(points)

    return {
        "points": points,
        "stats": {
            "gain": round(stats["elevation_gain"]),
            "loss": round(stats["elevation_loss"]),
            "max": round(stats["max_elevation"]),
            "min": round(stats["min_elevation"]),
        },
        "climbs": climbs,
    }


def sample_points(points: list[dict], interval_m: float = 30.0) -> list[dict]:
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


def calculate_cumulative_distances(points: list[dict]) -> list[dict]:
    """对轨迹点计算从起点累加的 Haversine 距离（米），返回带 dist 字段的点列表。"""
    if not points:
        return []
    result = [{**points[0], "dist": 0.0}]
    for i in range(1, len(points)):
        d = haversine_distance(
            points[i - 1]["lat"], points[i - 1]["lon"],
            points[i]["lat"], points[i]["lon"],
        )
        result.append({**points[i], "dist": result[-1]["dist"] + d})
    return result


def douglas_peucker_smooth(points: list[dict], epsilon: float = 5.0) -> list[dict]:
    """Douglas-Peucker 平滑：保留高程变化 >= epsilon 米的关键拐点，
    删除平缓段的冗余点。比移动平均更好地保留山顶、谷底等真实地形特征。

    对 (dist, ele) 序列做递归简化：
    - 找到距离首尾连线最远的点
    - 若垂直距离 >= epsilon 则保留该点并递归处理两侧
    - 否则中间所有点被舍弃（用直线连接首尾）
    """
    if len(points) <= 2:
        return list(points)

    # 在 (dist, ele) 空间中做 DP 简化，保留原始 lat/lon
    def perpendicular_distance(idx: int, start_idx: int, end_idx: int) -> float:
        """计算点到 start->end 连线的垂直距离（在 dist-ele 坐标系）。"""
        dx = points[end_idx]["dist"] - points[start_idx]["dist"]
        dy = points[end_idx]["ele"] - points[start_idx]["ele"]
        if dx == 0 and dy == 0:
            return 0.0
        # 点到直线的垂直距离
        ex = points[idx]["dist"] - points[start_idx]["dist"]
        ey = points[idx]["ele"] - points[start_idx]["ele"]
        # 叉积面积 / 底边长
        return abs(dx * ey - dy * ex) / _math.sqrt(dx * dx + dy * dy)

    def dp_recurse(start: int, end: int, result_indices: list[int]):
        """递归 DP 简化。"""
        max_dist = 0.0
        max_idx = start
        for i in range(start + 1, end):
            d = perpendicular_distance(i, start, end)
            if d > max_dist:
                max_dist = d
                max_idx = i

        if max_dist >= epsilon:
            dp_recurse(start, max_idx, result_indices)
            result_indices.append(max_idx)
            dp_recurse(max_idx, end, result_indices)

    indices = [0]
    dp_recurse(0, len(points) - 1, indices)
    indices.append(len(points) - 1)
    indices = sorted(set(indices))

    return [points[i] for i in indices]


# Savitzky-Golay 预计算系数：(系数列表, 归一化分母)
_SG_COEFFS = {
    (5, 2): ([-3, 12, 17, 12, -3], 35),
    (7, 2): ([-2, 3, 6, 7, 6, 3, -2], 21),
}


def savitzky_golay_smooth(points: list[dict], window: int = 5, order: int = 2) -> list[dict]:
    """Savitzky-Golay 平滑滤波，消除 DEM 高频噪声。points 需近似等间距。"""
    if len(points) < window:
        return list(points)
    half = window // 2
    coeffs, norm = _SG_COEFFS[(window, order)]
    n = len(points)
    result = []
    for i in range(n):
        if i < half or i >= n - half:
            result.append({**points[i]})
        else:
            ele = sum(
                points[i + j - half]["ele"] * coeffs[j]
                for j in range(window)
            ) / norm
            result.append({**points[i], "ele": round(ele, 1)})
    return result


def smooth_elevations(points: list[dict], window: int = 3) -> list[dict]:
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


def calculate_elevation_stats(points: list[dict], min_gain_threshold: float = 3.0) -> dict:
    """计算爬升统计。Douglas-Peucker 平滑去噪后累加正负高差。points 需含 ele 字段。
    若 points 无 dist 字段，自动使用累积 Haversine 距离计算。
    """
    # 防御性：确保有 dist 字段
    if points and "dist" not in points[0]:
        points = calculate_cumulative_distances(points)
    smoothed = savitzky_golay_smooth(points)
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
