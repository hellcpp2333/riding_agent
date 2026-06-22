## Context

当前 X 轴使用 `dist_km`（距离），但 Garmin 使用时间。切换回 `time_sec` 并格式化。

## Decisions

### 时间格式化函数

```js
function _fmtTime(sec) {
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = Math.floor(sec % 60);
  if (h > 0) return h + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
  return m + ':' + String(s).padStart(2, '0');
}
```

### 刻度间隔

- ≥1h → 每 10 分钟一个标签
- 30min-1h → 每 5 分钟
- <30min → 每 2 分钟
