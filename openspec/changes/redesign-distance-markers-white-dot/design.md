## Context

当前 `renderDistanceMarkers()` 生成的 HTML 结构为 flex column 布局：上方 span 显示 "{N} km"，下方 span 为灰色圆点。需改为单个白色圆点，数字居中嵌入。

## Goals / Non-Goals

**Goals:**
- 白色圆点（#fff），1px 深灰色边框（#3a3a3a）
- 纯数字（无单位），黑色（#1a1a1a），居中
- 圆点 22px 直径，字号 11px bold
- 不显示外部文字

**Non-Goals:**
- 不改变标记位置逻辑
- 不改变 5km 间隔

## Decisions

### 单 div 方案
- **决定**: 用一个 div 替代原先的两个 span + wrapper div。div 为白色圆形容器，内部直接放纯数字文字
- **样式**: `width:22px;height:22px;border-radius:50%;background:#fff;border:1.5px solid #3a3a3a;color:#1a1a1a;font-size:11px;font-weight:700;text-align:center;line-height:22px;box-shadow:0 1px 3px rgba(0,0,0,0.15)`
