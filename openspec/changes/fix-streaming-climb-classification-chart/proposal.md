## Why

上次迭代引入了流式回答、高程剖面和爬坡检测，但存在 3 个质量问题：1) 流式回答按 3 字符分块且有 10ms 延迟，不是真正的逐字流式效果；2) 爬坡段侧边栏中的海拔剖面图使用 `flex:1` 导致图表占满剩余空间过大，与 Garmin Connect 的 250px 固定高度设计不符；3) 爬坡分级使用自定义阈值（如 8%→HC），与 UCI（国际自行车联盟）标准分级规则不一致。

## What Changes

### 1. 真正的逐字流式
- SSE token 块大小从 3 字符改为 **1 字符**，延迟从 10ms 降为 **0**（无延迟）
- 前端 `sendMessage()` 的 SSE 处理已支持增量 token，只需减小 chunk size

### 2. 爬坡段面板剖面图缩小（参照 Garmin）
- `.climb-chart-container` 从 `flex: 1` 改为固定 `height: 250px`（与 Garmin `ClimbsSheet_chart` 高度一致）
- `#climb-canvas` 高度跟随容器

### 3. UCI 爬坡分级规则
参照 `refer/uci爬坡段分级规则.md`，替换当前自定义阈值为 UCI 标准：
- **准入条件**: 长度 ≥ 1000m **且** 平均坡度 ≥ 1.3%
- **分级公式**: UCI Score = 长度(km) × 平均坡度(%)²
- **阈值**:
  - 4级: Score < 60
  - 3级: Score 60–160
  - 2级: Score 160–330
  - 1级: Score 330–600
  - HC级: Score > 600

## Capabilities

### New Capabilities
- `uci-climb-classification`: 基于 UCI 标准公式的 5 级爬坡分类系统，准入条件为长度 ≥ 1000m 且坡度 ≥ 1.3%

### Modified Capabilities
- `climb-detection`: 分类算法从自定义阈值改为 UCI `km × grade²` 评分公式，分级阈值重新校准
- `streaming-chat-response`: token 分块大小从 3 字符改为 1 字符，移除延迟

## Impact

- **后端**: `app/services/elevation_service.py`（`classify_climb` 改为 UCI 公式 + 准入检查、`detect_climbs` 最小长度从 300m→1000m）
- **前端**: `static/index.html`（`classifyClimb` JS 函数同步改为 UCI 公式）、`static/css/style.css`（`.climb-chart-container` 高度 fix）
- **路由**: `app/api/v1/routes.py`（SSE chunk_size 3→1, sleep 10ms→0）
