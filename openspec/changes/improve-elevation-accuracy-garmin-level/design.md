## Context

当前系统使用 Open Elevation API 远程查询高程，受限于 HTTP 延迟和 API 调用次数，必须对路线点做 30m 等距采样（100km 路线约 3300 个请求点）。Garmin 使用本地 DEM 数据库 + 全点覆盖，精度远高于我们。本设计通过三步渐进优化逼近 Garmin 效果。

## Goals / Non-Goals

**Goals:**
1. GPX 自带高程不做平滑（保留设备气压计精度）
2. 采样密度翻倍（15m），爬升阈值降低（1m）
3. 本地 SRTM DEM 缓存，消除 API 限制，实现全量点查询
4. Douglas-Peucker 智能平滑替代移动平均

**Non-Goals:**
- 不购买付费高程 API
- 不改变前端高程面板 UI
- 不修改 `[ELEVATION_JSON]` 数据格式

## Decisions

### 1. 采样间隔: 30m → 15m
**理由**: SRTM 分辨率是 ~30m，15m 采样时相邻两个采样点可能落在同一 DEM 网格单元，但配合双线性插值可以提取子网格精度。100km 路线约 6600 个请求点，分 9 批（800/批），仍在 Open Elevation API 可接受范围内。切换到本地 DEM 后无此限制。

### 2. 平滑策略: 移动平均 → Douglas-Peucker
**理由**: 移动平均对所有点无差别平滑，会削平真实地形拐点（山顶、谷底）。Douglas-Peucker 保留高程变化 > epsilon 的特征点，删除平缓段冗余。epsilon=3m 对应约等于 SRTM 的垂直精度。

**算法**: 对 `(dist, ele)` 序列做 DP 简化，保留垂直变化 ≥3m 的拐点，线性连接平缓段。

### 3. 本地 SRTM DEM 架构

```
app/services/dem_service.py
├── class SRTMProvider
│   ├── __init__(data_dir="data/srtm/")
│   ├── _load_tile(lat, lon)      → 加载对应 HGT 文件
│   ├── get_elevation(lat, lon)   → 双线性插值查询
│   └── get_elevations(points)    → 批量查询
└── class ElevationProvider (facade)
    ├── try SRTMProvider first
    └── fallback to Open Elevation API
```

**SRTM HGT 格式**: 1 arc-second (~30m) 瓦片，3601×3601 网格（1°×1°）。中国区约需 30-50 个瓦片，~2-3GB。

**双线性插值**: 对于坐标 (lon, lat)，找到周围 4 个 DEM 网格点，按距离加权平均，消除阶梯状剖面。

### 4. GPX 高程处理
- `has_ele=True`: `smooth_elevations(window=1)` — 不平滑，直接使用设备数据
- `has_ele=False`: 本地 DEM 查询 + DP 平滑

## Risks / Trade-offs

1. **[SRTM 数据下载]** ~3GB 需要一次性下载。→ 提供下载脚本，按需下载覆盖中国区的瓦片列表。
2. **[rasterio 依赖较重]** rasterio 依赖 GDAL。→ 备选方案：直接用 struct 读取 HGT 原始二进制（无需 rasterio），HGT 格式非常简单（3601×3601 int16 大端）。
3. **[DP 平滑丢失极短起伏]** epsilon=3m 意味着 <3m 的起伏被忽略。→ 可配置，对中国丘陵地带 3m 是合理值。

## Open Questions

- HGT 二进制方案（无 rasterio 依赖）是否优先？→ 推荐，因为 HGT 格式极简，~20 行代码即可实现读取+插值，避免 GDAL 安装复杂性。
