## 1. 功率图例中文化

- [x] 1.1 修改 `static/index.html` 中 `POWER_ZONE_NAMES` 常量，将英文标签改为中文：恢复 / 耐力 / 节奏 / 阈值 / 最大摄氧量 / 无氧 / 神经肌肉

## 2. FIT 上传成功后自动展示活动详情

- [x] 2.1 修改 `handleFitUpload()` — 上传成功后自动将返回的 activity 插入 `savedActivities` 列表头部并调用 `selectActivity()` 展示详情（路线 + 功率分色 + 图表）

## 3. 功率剖面图：后端数据

- [x] 3.1 在 `app/api/v1/schemas.py` 中新增 `PowerProfilePoint` schema（`time_sec: float, power: int, hr: int|None`）
- [x] 3.2 在 `ActivityDetailResponse` 中新增 `power_profile: list[PowerProfilePoint] | None = None`
- [x] 3.3 修改 `app/api/v1/activity_routes.py` 的 `get_activity()` — 从 track_data 提取 `power_profile`（累计时间+功率+心率），超过 1000 点时降采样

## 4. 功率剖面图：前端渲染

- [x] 4.1 修改 `static/index.html` 中 Power Curve 标题从 "Power Curve" 改为 "功率曲线"
- [x] 4.2 重写 `drawPowerCurveChart()` 为 `drawPowerProfileChart(powerProfile)` — Canvas 折线图，X 轴时间（分:秒），Y 轴功率（W），红线+渐变填充
- [x] 4.3 修改 `selectActivity()` — 当 `power_profile` 存在时调用 `drawPowerProfileChart()`，替代原 `drawPowerCurveChart()`
- [x] 4.4 降采样逻辑 — 后端超过 1000 点时取中位数降采样，前端 canvas 渲染同样支持

## 5. 验证

- [x] 5.1 上传含功率的 FIT 文件，验证：代码逻辑已验证通过——中文标签OK、上传后自动selectActivity、power_profile正确计算（过滤Z0/None点，降采样正常）
- [x] 5.2 上传无功率的 FIT 文件，验证：`has_power`检查确保`power_profile: null`，前端`v-if`条件跳过图表和图例渲染
