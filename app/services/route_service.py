import math
import xml.etree.ElementTree as ET


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """计算两点间 Haversine 距离（米）"""
    r = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def parse_gpx(file_data: bytes) -> tuple[str, list[dict], float, float]:
    """解析 GPX 文件，返回 (name, track_points, total_distance_m, elevation_gain_m)"""
    try:
        root = ET.fromstring(file_data)
    except ET.ParseError:
        return ("", [], 0, 0)

    ns = {"gpx": "http://www.topografix.com/GPX/1/0"}
    ns_11 = {"gpx": "http://www.topografix.com/GPX/1/1"}

    name_el = root.find("gpx:name", ns)
    if name_el is None:
        name_el = root.find("gpx:name", ns_11)
    if name_el is None:
        name_el = root.find("name")
    name = name_el.text.strip() if name_el is not None and name_el.text else "未命名路书"

    points = []
    trkpt_elements = root.findall(".//gpx:trkpt", ns)
    if not trkpt_elements:
        trkpt_elements = root.findall(".//gpx:trkpt", ns_11)
    if not trkpt_elements:
        trkpt_elements = root.findall(".//trkpt")

    for pt in trkpt_elements:
        lat = float(pt.attrib.get("lat", 0))
        lon = float(pt.attrib.get("lon", 0))
        ele_el = pt.find("gpx:ele", ns)
        if ele_el is None:
            ele_el = pt.find("gpx:ele", ns_11)
        if ele_el is None:
            ele_el = pt.find("ele")
        ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0.0
        points.append({"lat": lat, "lon": lon, "ele": ele})

    distance = 0.0
    elevation_gain = 0.0
    for i in range(1, len(points)):
        d = haversine_distance(
            points[i - 1]["lat"], points[i - 1]["lon"],
            points[i]["lat"], points[i]["lon"],
        )
        distance += d
        ele_diff = points[i]["ele"] - points[i - 1]["ele"]
        if ele_diff > 0:
            elevation_gain += ele_diff

    return (name, points, distance, elevation_gain)


import os
import time
import uuid

import oss2

OSS_ACCESS_KEY_ID = os.environ.get("OSS_ACCESS_KEY_ID", "")
OSS_ACCESS_KEY_SECRET = os.environ.get("OSS_ACCESS_KEY_SECRET", "")
OSS_BUCKET_NAME = os.environ.get("OSS_BUCKET_NAME", "")
OSS_ENDPOINT = os.environ.get("OSS_ENDPOINT", "oss-cn-shenzhen.aliyuncs.com")

MAX_GPX_SIZE = 10 * 1024 * 1024  # 10 MB


def _get_bucket():
    auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
    return oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)


def upload_gpx_to_oss(file_data: bytes, filename: str, user_id: int) -> str:
    bucket = _get_bucket()
    ext = ".gpx"
    object_key = f"routes/{user_id}/{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
    bucket.put_object(object_key, file_data)
    return f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{object_key}"


def download_gpx_from_oss(oss_url: str) -> bytes:
    bucket = _get_bucket()
    object_key = _extract_object_key(oss_url)
    result = bucket.get_object(object_key)
    return result.read()


def delete_gpx_from_oss(oss_url: str) -> None:
    bucket = _get_bucket()
    try:
        object_key = _extract_object_key(oss_url)
        bucket.delete_object(object_key)
    except Exception:
        pass


def _extract_object_key(oss_url: str) -> str:
    prefix = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/"
    if oss_url.startswith(prefix):
        return oss_url[len(prefix):]
    return oss_url.split("/", 3)[-1] if "://" in oss_url else oss_url
