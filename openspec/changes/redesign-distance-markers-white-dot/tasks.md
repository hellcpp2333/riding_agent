## 1. 样式重构

- [ ] 1.1 替换 `renderDistanceMarkers()` 中的 labelContent 模板：用单个白色圆形 div（22px，白色背景，1.5px 深灰边框）替代原先的 flex column 双 span 结构
- [ ] 1.2 div 内部显示纯数字 `mp.distKm.toFixed(0)`（无"km"后缀），黑色 11px bold 字体，水平垂直居中
- [ ] 1.3 移除外部的距离文字标签和灰色圆点 span

## 2. 验证

- [ ] 2.1 规划一条路线，验证标记显示为白色圆点、内部纯数字、无外部文字，白色圆点盖过路线
