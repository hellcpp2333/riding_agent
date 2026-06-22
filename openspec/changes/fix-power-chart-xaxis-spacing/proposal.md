## Why

功率曲线 X 轴时间标签在小面板中因空间有限而重叠，弹窗大图间距也不足。

## What Changes

- 小图减少 X 轴刻度数（上调间隔阈值）
- 弹窗面板加宽（95vw / max 1400px），canvas 加高至 480px
- 弹窗图表同样放宽刻度间隔

## Impact

前端：`static/index.html` X 轴逻辑 + `static/css/style.css` 弹窗尺寸
