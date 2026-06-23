## 1. CSS adjustments

- [x] 1.1 Increase expanded canvas height from 600px to 750px for all chart types in `static/css/style.css`
- [x] 1.2 Increase modal panel max-width from 1600px to 1800px in `static/css/style.css`

## 2. JS expanded rendering parameters

- [x] 2.1 Increase padding from `{t:20, r:24, b:48, l:60}` to `{t:30, r:30, b:56, l:72}` in `drawTimeSeriesChartExpanded`
- [x] 2.2 Increase Y-axis font from 12px to 14px and tick count from 6 to 8 in `drawTimeSeriesChartExpanded`
- [x] 2.3 Increase X-axis font from 11px to 12px in `drawTimeSeriesChartExpanded`
- [x] 2.4 Reduce downsampling target from 2000 to 1000 points in `drawTimeSeriesChartExpanded`
- [x] 2.5 Increase avg line font from 11px to 12px to match X-axis in `drawTimeSeriesChartExpanded`

## 3. Verification

- [ ] 3.1 Open expanded speed chart — verify large clean panel
- [ ] 3.2 Open expanded cadence chart — verify large clean panel
- [ ] 3.3 Verify all 5 expanded charts share identical layout/sizing
