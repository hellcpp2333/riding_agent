"""骑行水平评估服务。

从历史活动数据估算 FTP、功体比、骑行等级，
并提供路线难度与用户体能的匹配评估。
"""

from __future__ import annotations

import math as _math
from typing import Any

from app.services.route_service import haversine_distance


def estimate_ftp_from_activities(activities: list[dict[str, Any]], user_weight_kg: float = 70.0) -> dict[str, Any]:
    """从最近 N 条活动记录估算 FTP 和骑行水平。

    activities: 最近的活动列表，每条含 power_curve 字典（按时间倒序，最新在前）
    user_weight_kg: 用户体重（默认 70kg）

    Returns: {"ftp": float, "ftp_wkg": float, "ftp_confidence": float,
              "fitness_level": str, "has_power": bool}
    """
    has_power = any(a.get("power_curve") and len(a.get("power_curve", {})) > 0 for a in activities)

    if not has_power:
        return _estimate_by_speed(activities, user_weight_kg)

    return _estimate_by_power(activities, user_weight_kg)


def _estimate_by_power(activities: list[dict[str, Any]], user_weight_kg: float) -> dict[str, Any]:
    """基于功率数据的 FTP 估算。"""
    from app.services.fit_service import merge_power_curves, compute_ftp_from_curve

    # 取最近 3 条有功率数据的活动
    powered = [a for a in activities if a.get("power_curve") and len(a.get("power_curve", {})) > 0]
    recent = powered[:3]

    ftps = []
    for act in recent:
        ftp = compute_ftp_from_curve(act["power_curve"])
        if ftp and ftp > 0:
            ftps.append(ftp)

    if not ftps:
        return _estimate_by_speed(activities, user_weight_kg)

    # 加权平均（时间越近权重越高）
    if len(ftps) == 1:
        ftp = ftps[0]
    elif len(ftps) == 2:
        ftp = ftps[0] * 0.6 + ftps[1] * 0.4
    else:
        ftp = ftps[0] * 0.5 + ftps[1] * 0.3 + ftps[2] * 0.2

    ftp = round(ftp, 1)
    ftp_wkg = round(ftp / user_weight_kg, 2) if user_weight_kg > 0 else 0
    confidence = min(0.9, 0.3 + len(ftps) * 0.2)  # 1条=0.5, 2条=0.7, 3条=0.9
    level = _classify_level(ftp_wkg)

    return {
        "ftp": ftp,
        "ftp_wkg": ftp_wkg,
        "ftp_confidence": confidence,
        "fitness_level": level,
        "has_power": True,
    }


def _estimate_by_speed(activities: list[dict[str, Any]], user_weight_kg: float) -> dict[str, Any]:
    """无功率数据时的经验分级（基于速度和爬升能力）。"""
    if not activities:
        return {
            "ftp": None, "ftp_wkg": None, "ftp_confidence": 0.0,
            "fitness_level": "beginner", "has_power": False,
        }

    # 取最近 5 条有距离和速度的活动
    recent = activities[:5]

    best_speed = max((a.get("avg_speed", 0) or 0 for a in recent), default=0)
    best_climb = 0.0  # m/h 爬升速度
    total_elev = 0.0
    total_dist = 0.0

    for a in recent:
        ele = a.get("elevation_gain", 0) or 0
        dist = a.get("distance", 0) or 0
        dur = a.get("duration", 0) or 0
        total_elev += ele
        total_dist += dist
        if dur > 0 and ele > 0:
            climb_rate = ele / (dur / 3600.0)  # m/h
            if climb_rate > best_climb:
                best_climb = climb_rate

    # 经验定级
    if best_speed >= 35 or best_climb > 800:
        level = "expert"
    elif best_speed >= 28 or best_climb > 500:
        level = "advanced"
    elif best_speed >= 22 or best_climb > 250:
        level = "amateur"
    else:
        level = "beginner"

    return {
        "ftp": None,
        "ftp_wkg": None,
        "ftp_confidence": 0.0,
        "fitness_level": level,
        "has_power": False,
    }


def _classify_level(ftp_wkg: float) -> str:
    """功体比 → 骑行等级。"""
    if ftp_wkg >= 4.5:
        return "pro"
    elif ftp_wkg >= 3.5:
        return "expert"
    elif ftp_wkg >= 2.5:
        return "advanced"
    elif ftp_wkg >= 1.5:
        return "amateur"
    return "beginner"


# ── 路线难度匹配 ──────────────────────────────────────────

def evaluate_route_difficulty(
    route_distance_m: float,
    route_elevation_m: float,
    estimated_time_s: float,
    user_fitness: dict[str, Any],
    user_weight_kg: float = 70.0,
) -> dict[str, Any]:
    """根据用户体能评估路线难度。

    Returns:
        {"fit_level": str, "estimated_completion": float,
         "ftp_required": float | None, "your_ftp": float | None,
         "key_challenges": list[str]}
    """
    challenges: list[str] = []

    # 需求功率简化估算
    # 平路巡航功率 ≈ (速度³ × CdA × ρ / 2 + 滚动阻力 × 体重 × g × 速度) / 效率
    # 爬坡功率 ≈ 体重 × g × 爬升速度
    # 简化为：VAM 代表爬坡能力，平路用速度估算

    avg_speed = route_distance_m / estimated_time_s if estimated_time_s > 0 else 5.0  # m/s
    vam = route_elevation_m / (estimated_time_s / 3600.0) if estimated_time_s > 0 else 0  # m/h

    # 粗略需求功率估算（平路 + 爬坡）
    grade = route_elevation_m / route_distance_m if route_distance_m > 0 else 0

    # 平路需求 (约 150W@30km/h for 70kg)
    flat_power = 150 * (avg_speed / 8.33) ** 1.5  # 速度修正，8.33 m/s = 30 km/h
    # 爬坡需求每 1% 坡度加约 35W
    climb_power = grade * 100 * 35
    total_power_needed = flat_power + climb_power
    ftp_required = round(total_power_needed * 0.85, 1)  # 0.85 效率修正

    # 匹配评估
    user_ftp = user_fitness.get("ftp")
    ftp_wkg = user_fitness.get("ftp_wkg") or 1.5

    if user_ftp is not None and user_ftp > 0:
        ratio = user_ftp / ftp_required if ftp_required > 0 else 99
        if ratio > 1.2:
            fit_level = "轻松"
        elif ratio >= 0.8:
            fit_level = "适合"
        elif ratio >= 0.5:
            fit_level = "有挑战"
        else:
            fit_level = "超出能力"
    else:
        # 无功率数据，用经验判断
        level = user_fitness.get("fitness_level", "beginner")
        if grade > 0.05:
            fit_level = "有挑战" if level in ("advanced", "expert") else "超出能力"
        elif grade > 0.03:
            fit_level = "适合" if level != "beginner" else "有挑战"
        else:
            fit_level = "轻松" if level != "beginner" else "适合"

    # 挑战点列表
    if vam > 800:
        challenges.append("爬升强度极大")
    elif vam > 500:
        challenges.append("爬升强度较大")
    if grade > 0.06:
        challenges.append("存在陡坡路段")
    if route_distance_m > 100000:
        challenges.append("超长距离，注意补给")
    elif route_distance_m > 60000:
        challenges.append("距离较长，建议带足补给")
    if ftp_required > 250 and not user_fitness.get("has_power", True):
        challenges.append("可能需要较好体能才能完成")

    return {
        "fit_level": fit_level,
        "estimated_completion": round(estimated_time_s, 0),
        "ftp_required": ftp_required,
        "your_ftp": user_ftp,
        "key_challenges": challenges or ["路线适中"],
    }
