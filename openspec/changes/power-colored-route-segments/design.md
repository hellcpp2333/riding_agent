## Context

当前 `fit_service.py` 解析 FIT 文件后，每条 record 已包含 `power` 字段（单位为瓦特），`compute_ride_summary()` 也计算了 FTP（功能阈值功率）。在 `drawActivityRoute()` 中，前端用单一红色 `BMapGL.Polyline` 渲染整条路线。这丢失了功率的时空分布信息。

参考 Garmin Connect 的活动详情页（refer/Garmin Connect.html），路线根据功率区间着色——共 7 个区间（Zone 1 到 Zone 7），颜色从灰/蓝（低强度）渐变到红/紫（高强度）。本设计复用此配色方案，结合百度地图 BMapGL API 实现。

现有爬坡段分色渲染（`drawClimbSegmentsOnMap`）已验证了"多段折线 + 颜色梯度"的技术可行性，功率分色在其基础上扩展即可。

## Goals / Non-Goals

**Goals:**
- 将路线轨迹点按功率区间聚合为连续路段
- 在地图上用 7 种颜色区分不同功率区间路段
- 显示功率区间图例
- 当 track_data 不含功率数据时，退回单色渲染（向后兼容）

**Non-Goals:**
- 不修改 FIT 文件解析逻辑（功率数据提取已就绪）
- 不实现功率区间统计面板（如各区间时长/占比），仅做地图可视化
- 不支持实时功率着色（仅处理已上传的 FIT 文件）
- 不添加用户自定义 FTP 配置 UI（使用自动计算的 FTP，若不可用则使用默认值 200W）

## Decisions

### 1. 功率区间模型：7 区 %FTP 模型

采用 Coggan 经典 7 区功率模型（与 Garmin 一致）：

| Zone | 名称 | %FTP 范围 | 颜色 |
|------|------|-----------|------|
| Z1 | Active Recovery | 0-55% | `#A0A0A0` (灰) |
| Z2 | Endurance | 55-75% | `#3498DB` (蓝) |
| Z3 | Tempo | 75-90% | `#2ECC71` (绿) |
| Z4 | Threshold | 90-105% | `#F1C40F` (黄) |
| Z5 | VO2Max | 105-120% | `#E67E22` (橙) |
| Z6 | Anaerobic | 120-150% | `#E74C3C` (红) |
| Z7 | Neuromuscular | >150% | `#8E44AD` (紫) |

**替代方案被否决**：
- 5 区模型（如 Strava）：粒度不够，Garmin 用户期望 7 区
- 连续色谱渐变：BMapGL Polyline 不支持渐变描边，且离散区间更易读

### 2. 路段聚合策略：贪心合并

遍历 track_data 轨迹点序列，维护当前路段的功率区间；当区间变化时封存当前路段并开启新路段。单个轨迹点功率为 0 或 None 时跳过（排除中断/滑行段），但这些点也归为 Z0（无数据），用透明或浅灰色标记。

**替代方案被否决**：
- 固定距离分块（如每 100m 一段）：区间边界不准确
- 滑动窗口平滑：增加延迟，离散区间本身已有平滑效果

### 3. 颜色定义：前端单一定义

颜色映射前端硬编码为 JavaScript 常量 `POWER_ZONE_COLORS`（复用 climb-gradient-color-scheme 模式），与爬坡颜色方案 `CLIMB_COLORS` 并列。后端只传递区间编号（0-7），不传颜色值。

### 4. API 数据格式

后端返回 `power_segments` 作为 `compute_ride_summary()` 的新增字段，或通过活动详情 API 返回：

```json
{
  "power_segments": [
    {"start_idx": 0, "end_idx": 142, "zone": 2, "avg_power": 145},
    {"start_idx": 143, "end_idx": 230, "zone": 4, "avg_power": 265},
    ...
  ]
}
```

每个 segment 的 `start_idx`/`end_idx` 索引 `track_data` 数组，前端据此切片渲染。

### 5. 前端渲染：多段 BMapGL.Polyline

参照 `drawClimbSegmentsOnMap()` 模式，对每个 power_segment 创建独立 `BMapGL.Polyline`，颜色取自 `POWER_ZONE_COLORS[zone]`。图例使用绝对定位的 HTML 元素叠加在地图角落。

### 6. FTP 获取策略

优先使用 `compute_ride_summary()` 已有的 `compute_ftp_from_curve()` 计算结果。若用户从未上传过含功率数据的 FIT 文件，使用默认 FTP 200W。

## Risks / Trade-offs

- **FTP 不准确**：自动 FTP 估算基于单次骑行的 Power Curve，可能与真实 FTP 有偏差 → 用户上传多次活动后 FTP 会更准确；后续可加手动 FTP 输入
- **功率缺失点**：FIT 文件中部分 record 可能无功率字段（设备不支持或信号丢失）→ 这些点标记为 Z0，渲染为浅灰色或跳过；连续 Z0 超过一定距离时不绘制
- **性能**：若轨迹点 >2000 个且区间切换频繁，可能产生上百段 polyline → 设定最小路段点数阈值（如 5 个点以上才单独成段），小段合并到相邻段
- **百度地图刷新**：多段 polyline 一次性添加到地图可能短暂卡顿 → 已在 `drawClimbSegmentsOnMap` 中验证，百段以内的 polyline 无明显性能问题

## Open Questions

- 是否需要在活动详情侧边栏也显示功率区间统计（时长/占比）？→ 当前 Non-goal，后续根据用户反馈决定
- 功率区间配色是否需要支持色盲友好模式？→ 后续可加
