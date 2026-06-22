## Why

功率分色路线功能（`power-colored-route-segments`）上线后有三处需要打磨：(1) 图例使用英文标籤，中文用户不易理解；(2) FIT 上传后缺乏明确的结果反馈，用户不确定数据是否已完整解析；(3) Power Curve 图表展示的是"各时长最佳平均功率"，非骑行过程中实际功率随时间的变化曲线，对分析单次骑行参考价值有限。本次改进提升这三处的用户体验。

## What Changes

- 功率区间图例标签改为中文：Z1 恢复 / Z2 耐力 / Z3 节奏 / Z4 阈值 / Z5 最大摄氧量 / Z6 无氧 / Z7 神经肌肉
- FIT 上传成功后自动展示活动摘要面板：在侧边栏显示姓名、距离、时长、爬升、功率等关键数据，替代纯文字 toast
- Power Curve 标题改为"功率曲线"，图表改为功率-时间剖面图：横轴为时间（分:秒），纵轴为功率（瓦特），完整展示整个骑行过程的功率变化

## Capabilities

### New Capabilities
- `power-profile-chart`: 功率-时间剖面图 — 替换 Power Curve 为骑行全程功率变化折线图，纵轴功率(W)，横轴时间

### Modified Capabilities
- `power-colored-map-render`: 图例标签语言从英文改为中文

## Impact

- **前端**: `static/index.html` — `POWER_ZONE_NAMES` 常量改为中文；`drawPowerCurveChart()` 重写为功率-时间剖面图；`handleFitUpload()` 增加上传成功后的详情展示
- **后端**: `app/api/v1/activity_routes.py` — 可能需要在 ActivityDetailResponse 中新增 `power_profile` 字段（时间+功率数组）供剖面图使用
- **样式**: `static/css/style.css` — 新增功率剖面图 canvas 样式
