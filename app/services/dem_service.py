"""本地 SRTM DEM 高程查询服务。

SRTM HGT 格式：1 arc-second (~30m) 瓦片，3601×3601 int16 大端网格。
每个瓦片覆盖 1°×1°，文件名: NXXEYYY.hgt（N=北纬, E=东经）。
数据源: https://dwtkns.com/srtm30m/ 或 https://step.esa.int/auxdata/dem/SRTM90/

中国区覆盖瓦片: N25E100 到 N45E130（约 50 个瓦片，~1.3GB）
"""

import math as _math
import os as _os
import struct as _struct
from pathlib import Path as _Path

# SRTM HGT 文件参数
_HGT_SIZE = 3601  # 1 arc-second SRTM grid width/height
_HGT_BYTES = _HGT_SIZE * _HGT_SIZE * 2  # 25,934,402 bytes
_HGT_RES = 1.0 / _HGT_SIZE  # ~0.0002778 degrees per cell

# 默认数据目录
DEFAULT_DEM_DIR = _Path(__file__).resolve().parent.parent.parent / "data" / "srtm"


class SRTMProvider:
    """SRTM HGT 高程查询器。直接读取二进制 HGT 文件，双线性插值。"""

    def __init__(self, data_dir: str | _Path = DEFAULT_DEM_DIR):
        self._data_dir = _Path(data_dir)
        self._cache: dict[str, list[list[int]] | None] = {}

    def _tile_path(self, lat: float, lon: float) -> _Path:
        """根据坐标获取 HGT 文件路径。"""
        lat_int = int(_math.floor(lat))
        lon_int = int(_math.floor(lon))
        lat_dir = "N" if lat_int >= 0 else "S"
        lon_dir = "E" if lon_int >= 0 else "W"
        filename = f"{lat_dir}{abs(lat_int):02d}{lon_dir}{abs(lon_int):03d}.hgt"
        return self._data_dir / filename

    def _load_tile(self, lat: float, lon: float) -> list[list[int]] | None:
        """加载 HGT 瓦片到内存。返回 3601×3601 二维列表或 None（文件不存在）。"""
        path = self._tile_path(lat, lon)
        cache_key = str(path)

        if cache_key in self._cache:
            return self._cache[cache_key]

        if not path.exists():
            self._cache[cache_key] = None
            return None

        try:
            with open(path, "rb") as f:
                raw = f.read()
            if len(raw) != _HGT_BYTES:
                self._cache[cache_key] = None
                return None

            # 解析 int16 大端
            grid = []
            for row in range(_HGT_SIZE):
                offset = row * _HGT_SIZE * 2
                row_data = list(_struct.unpack_from(f">{_HGT_SIZE}h", raw, offset))
                grid.append(row_data)
            self._cache[cache_key] = grid
            return grid
        except Exception:
            self._cache[cache_key] = None
            return None

    def get_elevation(self, lat: float, lon: float) -> float | None:
        """查询单个坐标的高程（米），双线性插值。返回 None 表示瓦片不存在。"""
        grid = self._load_tile(lat, lon)
        if grid is None:
            return None

        # 瓦片原点：左下角（整数经纬度）
        tile_lat = _math.floor(lat)
        tile_lon = _math.floor(lon)

        # 在网格内的浮点位置（0 到 _HGT_SIZE-1）
        frac_lat = (lat - tile_lat) / _HGT_RES
        frac_lon = (lon - tile_lon) / _HGT_RES

        row = int(_math.floor(frac_lat))
        col = int(_math.floor(frac_lon))

        # 边界裁剪
        row = max(0, min(row, _HGT_SIZE - 2))
        col = max(0, min(col, _HGT_SIZE - 2))

        dr = frac_lat - row
        dc = frac_lon - col

        # HGT 文件中第 0 行 = 瓦片北边界（高纬度），所以需要翻转
        # SRTM HGT: row 0 = northernmost (largest lat)
        # 我们的 grid 从上到下存储，row 0 对应 _HGT_SIZE-1 实际行
        hgt_row = _HGT_SIZE - 1 - row
        hgt_row_next = _HGT_SIZE - 1 - (row + 1)

        # 4 个相邻格点的高程
        z00 = grid[hgt_row][col]        # 左下
        z10 = grid[hgt_row_next][col]   # 左上
        z01 = grid[hgt_row][col + 1]    # 右下
        z11 = grid[hgt_row_next][col + 1]  # 右上

        # 无效值处理（SRTM 海洋/空洞 = -32768）
        values = [z00, z10, z01, z11]
        valid = [v for v in values if v > -1000]
        if not valid:
            return 0.0  # 水域
        # 用有效值的平均替代无效值
        avg_valid = sum(valid) / len(valid)
        if z00 <= -1000:
            z00 = avg_valid
        if z10 <= -1000:
            z10 = avg_valid
        if z01 <= -1000:
            z01 = avg_valid
        if z11 <= -1000:
            z11 = avg_valid

        # 双线性插值
        z0 = z00 + (z10 - z00) * dr
        z1 = z01 + (z11 - z01) * dr
        return float(z0 + (z1 - z0) * dc)

    def get_elevations(self, points: list[dict]) -> list[dict]:
        """批量查询高程。points: [{"lat": x, "lon": y}, ...]
        返回: [{"lat": x, "lon": y, "ele": z}, ...]
        """
        results = []
        for p in points:
            ele = self.get_elevation(p["lat"], p["lon"])
            results.append({
                "lat": p["lat"],
                "lon": p["lon"],
                "ele": ele if ele is not None else 0.0,
            })
        return results

    def has_tile(self, lat: float, lon: float) -> bool:
        """检查瓦片是否存在。"""
        return self._tile_path(lat, lon).exists()

    def clear_cache(self):
        """清空瓦片缓存。"""
        self._cache.clear()


# 全局单例
_srtm_provider: SRTMProvider | None = None
_use_local_dem: bool | None = None


def _get_srtm_provider() -> SRTMProvider | None:
    """延迟加载 SRTM provider。"""
    global _srtm_provider, _use_local_dem
    if _srtm_provider is None and _use_local_dem is None:
        _srtm_provider = SRTMProvider()
        # 检查 data/srtm/ 目录下是否有 .hgt 瓦片
        _use_local_dem = any(
            p.suffix == '.hgt' for p in _srtm_provider._data_dir.iterdir()
        )
        if not _use_local_dem:
            _srtm_provider = None
    return _srtm_provider


def lookup_elevations_local(points: list[dict]) -> list[dict]:
    """高程查询——本地 SRTM DEM 优先，自动 fallback 到 Open Elevation API。

    用法与 lookup_elevations_batched 相同，直接替换即可。
    """
    srtm = _get_srtm_provider()
    if srtm is not None:
        try:
            return srtm.get_elevations(points)
        except Exception:
            pass

    # Fallback: 远程 API 查询
    from app.services.elevation_service import lookup_elevations_batched
    return lookup_elevations_batched(points)


def local_dem_available() -> bool:
    """检查本地 DEM 是否可用。"""
    srtm = _get_srtm_provider()
    return srtm is not None


CHINA_SRTM_TILES = [
    # 经纬度范围: 18°N-54°N, 73°E-135°E
    # 常用骑行区域（华北/华东/华中）
    (f"{lat_dir}{abs(lat):02d}{lon_dir}{abs(lon):03d}.hgt", lat, lon)
    for lat in range(18, 55)
    for lon in range(73, 136)
    for lat_dir, lon_dir in [("N", "E")]
]


def print_download_help():
    """打印 SRTM 瓦片下载说明。"""
    print("""
SRTM 1 arc-second (~30m) DEM 数据下载说明:

数据源:
  https://step.esa.int/auxdata/dem/SRTM90/  (ESA, 免费注册)
  https://dwtkns.com/srtm30m/                 (便捷下载)

下载步骤:
  1. 访问上述 URL
  2. 下载覆盖目标区域的 HGT 文件（每个 1°×1°）
  3. 放入 data/srtm/ 目录

中国区常用瓦片（北京）:
  N39E116.hgt  N40E116.hgt
  N39E117.hgt  N40E117.hgt

初始化后自动检测 data/srtm/ 下是否有可用瓦片。
有瓦片 → 本地毫秒级查询；无瓦片 → 自动 fallback Open Elevation API。
""")
