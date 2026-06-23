## 1. CSS adjustments

- [x] 1.1 Increase expanded canvas height from 480px to 600px for all chart types in `static/css/style.css`
- [x] 1.2 Increase modal panel max-width from 1400px to 1600px in `static/css/style.css`

## 2. JS X-axis tick spacing

- [x] 2.1 Widen X-axis tick intervals in `drawTimeSeriesChartExpanded`: change from `totalMin > 180 ? 15 : totalMin > 60 ? 10 : totalMin > 30 ? 5 : 2` to `totalMin > 240 ? 20 : totalMin > 120 ? 15 : totalMin > 60 ? 10 : 5`

## 3. Verification

- [ ] 3.1 Open expanded speed chart — verify larger panel, wider tick spacing
- [ ] 3.2 Open expanded cadence chart — verify larger panel, wider tick spacing
- [ ] 3.3 Open expanded power chart — verify it still looks correct with new sizing
