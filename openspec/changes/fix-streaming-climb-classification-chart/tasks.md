## 1. 逐字流式回答

- [x] 1.1 `routes.py`: `/api/chat` 中 `chunk_size` 从 3 改为 1
- [x] 1.2 `routes.py`: `/api/chat` 中移除 `await asyncio.sleep(0.01)` 延迟
- [x] 1.3 `routes.py`: `/api/route/plan` 中同样 chunk_size=1, 移除 sleep
- [x] 1.4 验证：发送对话，确认前端逐字显示（无 3 字分组现象）

## 2. 爬坡面板剖面图缩小

- [x] 2.1 `style.css`: `.climb-chart-container` 从 `flex:1;min-height:200px` 改为 `height:250px;flex-shrink:0`
- [x] 2.2 `style.css`: `#climb-canvas` 从 `width:100%;height:100%` 改为明确尺寸适应 250px 容器
- [x] 2.3 验证：打开爬坡段侧边栏，确认图表不再占满整个面板高度

## 3. UCI 爬坡分级规则

- [x] 3.1 `elevation_service.py`: `classify_climb()` 改用 UCI 公式 `Score = km × grade²`，按新阈值分级
- [x] 3.2 `elevation_service.py`: `classify_climb()` 新增准入条件判断（长度 < 1000m 或坡度 < 1.3% → 不评级）
- [x] 3.3 `elevation_service.py`: `detect_climbs()` 最小坡段长度从 300m 改为 1000m
- [x] 3.4 `index.html`: `classifyClimb()` JS 函数同步改为 UCI 公式 + 新阈值
- [x] 3.5 验证：规划含爬坡路线，确认分级标签正确（如妙峰山约 20km@5.5% ≈ 605→HC）

## 4. 清理与验证

- [x] 4.1 删除 `index.html` 中不再使用的 `detectClimbSegments()` 函数
- [x] 4.2 完整测试：规划路线 → 确认逐字流式 + 爬坡 UCI 分级 + 面板图表 250px
