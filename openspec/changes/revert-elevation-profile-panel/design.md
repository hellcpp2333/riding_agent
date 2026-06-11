## Context

当前 `static/index.html` 的工作树修改引入了三个主要 UI 区域变更：
1. 地图容器从全高度拆分为 `#map-area`（75%）+ `#elevation-panel`（25%）flex 纵向布局
2. `#elevation-panel` 内包含 stats 卡片（距离/爬升/下降）和 Canvas 海拔剖面图
3. `#climb-sidebar` 从右侧滑入显示爬坡段详情

后端方面，agent.py 在工具调用结果后附加 `[ELEVATION_JSON]` 结构化数据块，routes.py 解析该块发送独立 `elevation` SSE 事件。

这些变更均未提交（仅在工作树），回退路径清晰。

## Goals / Non-Goals

**Goals:**
- 移除所有海拔剖面图 UI（面板、侧边栏、Canvas）
- 移除后端为面板服务的结构化数据通路
- 恢复地图容器为全高度 100% 展示
- 保持高程文本摘要（`[高程数据]`）在聊天消息中继续显示

**Non-Goals:**
- 不移除 open-elevation 高程查询服务
- 不移除坐标转换（BD-09 → WGS-84）
- 不移除高程统计（gain/loss/min/max）计算
- 不移除 favicon

## Decisions

### 1. 保留高程文本信息，仅移除可视化面板
- **决定**: 保留 agent.py 中 `[高程数据]` 文本摘要输出，仅移除 `[ELEVATION_JSON]` 及 `calculate_cumulative_distances` 调用
- **理由**: 高程统计（累计爬升/下降/最高点/最低点）在聊天消息中有独立价值，用户仍可看到文字形式的数据

### 2. 通过 git checkout 恢复前端文件最安全
- **决定**: 对 `static/index.html` 和 `static/css/style.css` 使用 `git checkout HEAD -- <file>` 恢复到最后提交状态
- **替代方案**: 手动逐块删除 —— 更精确但易出错，因为 index.html 有 470+ 行新增
- **理由**: 这两个文件的所有工作树修改均属于剖面图功能，直接恢复可确保干净回退

### 3. 后端文件手动修改
- **决定**: agent.py、routes.py、elevation_service.py 采用精确 Edit 方式修改
- **理由**: 后端文件修改量小（各约 10-20 行），且需保留高程服务核心逻辑，手动编辑更精确

## Risks / Trade-offs

- [Risk] 前端文件 `git checkout` 会丢失 favicon 添加 → 在 checkout 后重新添加 favicon `<link>` 标签
- [Trade-off] 移除 `calculate_cumulative_distances` 后，若未来重新需要海拔剖面图，需重新实现 → 函数逻辑简单（Haversine 累加），重新实现成本低
