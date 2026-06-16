"""FIT 文件解析与骑行数据分析服务。

解析 Garmin/码表 FIT 文件，提取轨迹、功率、心率、踏频等数据，
计算 Power Curve、NP（标准化功率）、TSS（训练压力）、IF（强度因子）。
"""

import math as _math
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from io import BytesIO
from typing import Any
from xml.etree import ElementTree as _ET

from app.services.route_service import haversine_distance


# 关键时长列表（秒），用于 Power Curve 构建
POWER_CURVE_DURATIONS = [5, 30, 60, 300, 600, 1200, 1800, 2400, 3600]


def parse_fit(file_data: bytes) -> dict[str, Any]:
    """解析 FIT 二进制文件，返回提取的骑行数据字典。

    Returns:
        {
            "name": str,
            "start_time": datetime,
            "device_info": str,
            "records": [{"timestamp": int, "lat": float, "lon": float,
                         "altitude": float, "heart_rate": int, "power": int,
                         "cadence": int, "speed": float, "distance": float}, ...],
            "sessions": [{"start_time": ..., "total_distance": ..., "total_elapsed_time": ...,
                          "avg_heart_rate": ..., "avg_power": ..., "avg_cadence": ..., ...}],
            "laps": [...],
        }
    """
    import fitdecode
    from fitdecode import FitReader

    records: list[dict] = []
    sessions: list[dict] = []
    laps: list[dict] = []
    name = ""
    start_time: datetime | None = None
    device_info = ""

    try:
        with FitReader(BytesIO(file_data)) as fit:
            for frame in fit:
                if not isinstance(frame, fitdecode.records.FitDataMessage):
                    continue

                msg = frame
                msg_name = msg.name

                if msg_name == "record":
                    rec = _extract_record(msg)
                    records.append(rec)
                elif msg_name == "session":
                    sessions.append(_extract_session(msg))
                elif msg_name == "lap":
                    laps.append(_extract_lap(msg))
                elif msg_name == "file_id":
                    if start_time is None and msg.has_field("time_created"):
                        start_time = msg.get_value("time_created")
                elif msg_name == "device_info":
                    device_info = _extract_device(msg)
                elif msg_name == "sport" and not name:
                    if msg.has_field("name"):
                        name = msg.get_value("name")
    except Exception:
        raise ValueError("无法解析 FIT 文件，请确认文件格式正确且未损坏")

    if not records:
        raise ValueError("FIT 文件中未找到骑行记录数据")

    if not name:
        name = "骑行活动"

    if start_time is None and records:
        start_time = _ts_to_datetime(records[0].get("timestamp", 0))

    return {
        "name": name,
        "start_time": start_time,
        "device_info": device_info,
        "records": records,
        "sessions": sessions,
        "laps": laps,
    }


def compute_ride_summary(records: list[dict]) -> dict[str, Any]:
    """从 record 列表计算骑行摘要：距离、时长、速度、心率、功率、踏频、NP/TSS/IF。"""
    if not records:
        return _empty_summary()

    total_dist = 0.0
    total_time = 0.0
    hr_sum = 0.0
    power_sum = 0.0
    cad_sum = 0.0
    hr_count = 0
    power_count = 0
    cad_count = 0
    max_hr = 0
    max_power = 0
    total_ele_gain = 0.0
    prev_alt = None

    # 功率点列表（用于 NP 和 Power Curve）
    power_samples: list[tuple[int, int]] = []  # [(timestamp, power), ...]
    elapsed_sec = 0.0

    # 轨迹点
    track: list[dict] = []

    for i, r in enumerate(records):
        ts = r.get("timestamp", 0)
        lat = r.get("lat")
        lon = r.get("lon")
        alt = r.get("altitude")
        hr = r.get("heart_rate")
        power = r.get("power")
        cad = r.get("cadence")
        speed = r.get("speed", 0)
        dist = r.get("distance", 0)

        # 累计距离
        if i > 0 and lat is not None and lon is not None:
            prev = track[-1]
            if prev.get("lat") is not None and prev.get("lon") is not None:
                total_dist += haversine_distance(
                    prev["lat"], prev["lon"], lat, lon
                )

        # 时间
        if i > 0:
            prev_ts = records[i - 1].get("timestamp", ts)
            dt = ts - prev_ts
            if 0 < dt < 300:  # 忽略暂停（>5分钟间隔）
                total_time += dt

        # 心率
        if hr is not None and hr > 0:
            hr_sum += hr
            hr_count += 1
            if hr > max_hr:
                max_hr = hr

        # 功率
        if power is not None and power > 0:
            power_sum += power
            power_count += 1
            if power > max_power:
                max_power = power
            power_samples.append((ts, power))

        # 踏频
        if cad is not None and cad > 0:
            cad_sum += cad
            cad_count += 1

        # 累计爬升
        if alt is not None and prev_alt is not None and alt > prev_alt:
            total_ele_gain += alt - prev_alt
        if alt is not None:
            prev_alt = alt

        track.append({
            "lat": lat,
            "lon": lon,
            "ele": alt,
            "hr": hr,
            "power": power,
            "cadence": cad,
            "speed": speed,
            "timestamp": ts,
        })

    avg_speed = (total_dist / total_time * 3.6) if total_time > 0 else 0.0
    avg_hr = hr_sum / hr_count if hr_count > 0 else 0
    avg_power = power_sum / power_count if power_count > 0 else 0
    avg_cad = cad_sum / cad_count if cad_count > 0 else 0

    # NP / TSS / IF
    np_val = compute_np(power_samples)
    ftp_for_tss = compute_ftp_from_curve(build_power_curve(power_samples)) or 200
    intensity = np_val / ftp_for_tss if ftp_for_tss > 0 else 0
    tss_val = compute_tss(np_val, intensity, total_time) if total_time > 0 else 0

    # Power Curve
    power_curve = build_power_curve(power_samples)

    # 心率区间
    hr_zones = compute_hr_zones(records) if max_hr > 0 else {}

    return {
        "distance": round(total_dist, 1),
        "duration": round(total_time, 1),
        "elevation_gain": round(total_ele_gain, 1),
        "avg_speed": round(avg_speed, 1),
        "avg_hr": round(avg_hr, 1),
        "avg_power": round(avg_power, 1) if power_count > 0 else None,
        "avg_cadence": round(avg_cad, 1) if cad_count > 0 else None,
        "max_hr": max_hr,
        "max_power": max_power if power_count > 0 else None,
        "np": round(np_val, 1) if power_count > 0 else None,
        "tss": round(tss_val, 1) if power_count > 0 else None,
        "if_score": round(intensity, 2) if power_count > 0 else None,
        "power_curve": power_curve,
        "hr_zones": hr_zones,
        "track_points": len(track),
        "track_data": track,
    }


def build_power_curve(power_samples: list[tuple[int, int]]) -> dict[str, float]:
    """构建 Power Curve：各时长最佳平均功率。

    power_samples: [(timestamp, power), ...] 按时间排序
    Returns: {"5": 800.0, "30": 650.0, "60": 520.0, ...}
    """
    if not power_samples:
        return {}

    n = len(power_samples)
    curve: dict[str, float] = {}

    for dur in POWER_CURVE_DURATIONS:
        best = 0.0
        # 滑动窗口计算该时长的最大平均功率
        j = 0
        window_sum = 0
        window_count = 0
        for i in range(n):
            # 扩展窗口右边界
            while j < n and (power_samples[j][0] - power_samples[i][0]) <= dur:
                window_sum += power_samples[j][1]
                window_count += 1
                j += 1
            # 计算窗口平均
            if window_count > 0:
                avg = window_sum / window_count
                if avg > best:
                    best = avg
            # 收缩窗口左边界
            window_sum -= power_samples[i][1]
            window_count -= 1

        if best > 0:
            curve[str(dur)] = round(best, 1)

    return curve


def merge_power_curves(curves: list[dict[str, float]]) -> dict[str, float]:
    """合并多个 Power Curve，每个时长取最大值。"""
    merged: dict[str, float] = {}
    for curve in curves:
        for dur, val in curve.items():
            if dur not in merged or val > merged[dur]:
                merged[dur] = val
    return merged


def compute_ftp_from_curve(power_curve: dict[str, float]) -> float | None:
    """从 Power Curve 多时长加权推导 FTP。

    候选：
      - 20min × 0.95
      - 30min × 0.97
      - 40min × 0.99
      - 60min × 1.00

    权重：20m=0.3, 30m=0.3, 40m=0.2, 60m=0.2
    """
    candidates: list[tuple[float, float]] = []

    mapping = [
        ("1200", 0.95, 0.3),
        ("1800", 0.97, 0.3),
        ("2400", 0.99, 0.2),
        ("3600", 1.00, 0.2),
    ]

    for dur_key, factor, weight in mapping:
        if dur_key in power_curve and power_curve[dur_key] > 0:
            ftp_candidate = power_curve[dur_key] * factor
            candidates.append((ftp_candidate, weight))

    if not candidates:
        # 退到可用的最长时长 × 0.95
        for dur_key in ["3600", "2400", "1800", "1200", "600", "300"]:
            if dur_key in power_curve and power_curve[dur_key] > 0:
                return round(power_curve[dur_key] * 0.95, 1)
        return None

    # 加权平均
    total_weight = sum(w for _, w in candidates)
    if total_weight == 0:
        return None

    weighted_sum = sum(v * w for v, w in candidates)
    # 归一化
    ftp = weighted_sum / total_weight

    return round(ftp, 1)


def compute_np(power_samples: list[tuple[int, int]]) -> float:
    """计算标准化功率 (Normalized Power)。

    NP = (30秒平滑平均功率⁴ 的均值) ^ 0.25
    """
    if not power_samples:
        return 0.0

    # 30秒滚动平均功率
    smoothed = []
    window = 30
    for i in range(len(power_samples)):
        start_ts = power_samples[i][0] - window
        total = 0.0
        count = 0
        for j in range(i, -1, -1):
            if power_samples[j][0] >= start_ts:
                total += power_samples[j][1]
                count += 1
            else:
                break
        if count > 0:
            smoothed.append(total / count)

    if not smoothed:
        return 0.0

    # 四次方均值，开四次方
    sum_p4 = sum(p ** 4 for p in smoothed)
    mean_p4 = sum_p4 / len(smoothed)
    return round(mean_p4 ** 0.25, 1)


def compute_tss(np_val: float, intensity: float, duration_sec: float) -> float:
    """计算训练压力分数 (Training Stress Score)。

    TSS = (NP / FTP)² × 持续时间(小时) × 100
    简化：TSS = IF² × 小时 × 100
    """
    hours = duration_sec / 3600.0
    return round(intensity ** 2 * hours * 100, 1)


def compute_hr_zones(records: list[dict], max_hr: int | None = None) -> dict[str, float]:
    """计算心率区间分布（时间百分比）。

    区间划分（%最大心率）：
      Z1: < 60%, Z2: 60-70%, Z3: 70-80%, Z4: 80-90%, Z5: > 90%
    """
    if not max_hr:
        max_hr = max((r.get("heart_rate") or 0 for r in records), default=0)
    if max_hr <= 0:
        return {}

    zones = {"Z1": 0.0, "Z2": 0.0, "Z3": 0.0, "Z4": 0.0, "Z5": 0.0}
    total_time = 0.0

    for i in range(1, len(records)):
        hr = records[i].get("heart_rate")
        if hr is None or hr <= 0:
            continue
        dt = records[i].get("timestamp", 0) - records[i - 1].get("timestamp", 0)
        if dt <= 0 or dt > 300:
            continue
        total_time += dt
        pct = hr / max_hr
        if pct < 0.6:
            zones["Z1"] += dt
        elif pct < 0.7:
            zones["Z2"] += dt
        elif pct < 0.8:
            zones["Z3"] += dt
        elif pct < 0.9:
            zones["Z4"] += dt
        else:
            zones["Z5"] += dt

    if total_time > 0:
        for k in zones:
            zones[k] = round(zones[k] / total_time * 100, 1)

    return zones


# ── 内部辅助 ──────────────────────────────────────────────

def _extract_record(msg) -> dict:
    """从 FIT record 消息提取字段。"""
    fields = {
        "timestamp": 0, "lat": None, "lon": None, "altitude": None,
        "heart_rate": None, "power": None, "cadence": None,
        "speed": None, "distance": None,
    }
    for fd in msg.fields:
        name = fd.name
        if name == "timestamp":
            fields[name] = _ts_to_timestamp(fd.value)
        elif name == "position_lat":
            fields["lat"] = _semicircles_to_deg(fd.value) if fd.value is not None else None
        elif name == "position_long":
            fields["lon"] = _semicircles_to_deg(fd.value) if fd.value is not None else None
        elif name == "altitude":
            fields[name] = round(fd.value, 1) if fd.value is not None else None
        elif name == "heart_rate":
            fields[name] = int(fd.value) if fd.value is not None else None
        elif name == "power":
            fields[name] = int(fd.value) if fd.value is not None else None
        elif name == "cadence":
            fields[name] = int(fd.value) if fd.value is not None else None
        elif name == "speed":
            fields[name] = round(fd.value, 2) if fd.value is not None else None
        elif name == "distance":
            fields[name] = round(fd.value, 1) if fd.value is not None else None
    return fields


def _extract_session(msg) -> dict:
    """从 FIT session 消息提取汇总字段。"""
    result = {}
    for fd in msg.fields:
        val = fd.value
        if fd.name == "start_time":
            result["start_time"] = str(val) if val is not None else None
        elif fd.name == "total_distance":
            result["total_distance"] = round(val, 1) if val is not None else 0
        elif fd.name == "total_elapsed_time":
            result["total_elapsed_time"] = round(val, 1) if val is not None else 0
        elif fd.name == "avg_heart_rate":
            result["avg_heart_rate"] = round(val, 1) if val is not None else None
        elif fd.name == "avg_power":
            result["avg_power"] = round(val, 1) if val is not None else None
        elif fd.name == "avg_cadence":
            result["avg_cadence"] = round(val, 1) if val is not None else None
        elif fd.name == "sport":
            result["sport"] = str(val) if val is not None else None
        elif fd.name == "enhanced_avg_speed":
            result["avg_speed"] = round(val, 3) if val is not None else None
        elif fd.name == "total_ascent":
            result["total_ascent"] = round(val, 1) if val is not None else 0
        elif fd.name == "total_calories":
            result["total_calories"] = int(val) if val is not None else 0
    return result


def _extract_lap(msg) -> dict:
    """从 FIT lap 消息提取字段。"""
    result = {}
    for fd in msg.fields:
        val = fd.value
        if fd.name == "start_time":
            result["start_time"] = str(val) if val is not None else None
        elif fd.name == "total_distance":
            result["total_distance"] = round(val, 1) if val is not None else 0
        elif fd.name == "total_elapsed_time":
            result["total_elapsed_time"] = round(val, 1) if val is not None else 0
        elif fd.name == "avg_heart_rate":
            result["avg_heart_rate"] = round(val, 1) if val is not None else None
        elif fd.name == "avg_power":
            result["avg_power"] = round(val, 1) if val is not None else None
    return result


def _extract_device(msg) -> str:
    """从 device_info 消息提取设备名称。"""
    parts = []
    for fd in msg.fields:
        if fd.name in ("manufacturer", "product_name", "serial_number"):
            if fd.value is not None:
                parts.append(str(fd.value))
    return " ".join(parts) if parts else ""


def _semicircles_to_deg(sc: int) -> float:
    """半圆 → 度（Garmin FIT 坐标格式）。"""
    return sc * (180.0 / 2**31)


def _ts_to_timestamp(raw) -> int:
    """将 FIT 时间戳转为 Unix 秒。FIT epoch = 1989-12-31 00:00:00 UTC。"""
    if isinstance(raw, datetime):
        return int(raw.timestamp())
    if isinstance(raw, (int, float)):
        fit_epoch = datetime(1989, 12, 31, tzinfo=timezone.utc).timestamp()
        return int(raw + fit_epoch)
    return 0


def _ts_to_datetime(ts: int) -> datetime | None:
    if ts <= 0:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def _empty_summary() -> dict:
    return {
        "distance": 0, "duration": 0, "elevation_gain": 0,
        "avg_speed": 0, "avg_hr": 0, "avg_power": None,
        "avg_cadence": None, "max_hr": 0, "max_power": None,
        "np": None, "tss": None, "if_score": None,
        "power_curve": {}, "hr_zones": {}, "track_points": 0, "track_data": [],
    }
