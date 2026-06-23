## Why

The expanded (modal) charts for cadence and speed remain too small with overly dense coordinate rendering despite previous adjustments. The shared `drawTimeSeriesChartExpanded` function, while structurally correct, uses parameters that don't match the original power chart expanded view the user was satisfied with. The expanded panel needs to match the power chart's design exactly.

## What Changes

- Increase expanded canvas height from 600px to 750px
- Increase modal max-width from 1600px to 1800px
- Increase chart padding (more breathing room around the plot area)
- Increase font sizes in expanded view (14px Y-axis labels, 12px X-axis labels)
- Reduce downsampling target from 2000 to 1000 points for cleaner lines
- Increase Y-axis tick count from 6 to 8 for finer value granularity
- Apply universally to all 5 expanded chart types

## Capabilities

### New Capabilities
- `expanded-chart-sizing`: Larger, cleaner expanded chart rendering with reduced data density and improved readability

## Impact

- **JS**: `static/index.html` — `drawTimeSeriesChartExpanded` function (padding, fonts, downsampling, tick count)
- **CSS**: `static/css/style.css` — canvas height and modal max-width
