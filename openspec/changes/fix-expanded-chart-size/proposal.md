## Why

The expanded (modal) charts for cadence and speed appear too small with overly dense X-axis tick marks, making them harder to read than the power chart's expanded view. The modal panel canvas height (480px) and X-axis tick interval logic inherited from the power chart don't suit the visual characteristics of cadence/speed data.

## What Changes

- Increase expanded modal canvas height from 480px to 600px for all chart types
- Increase modal panel max-width from 1400px to 1600px
- Widen X-axis tick intervals in the expanded view: minimum interval 5min (was 2min), use larger steps for longer rides
- Apply same improvements uniformly to all chart expanded views (power, speed, HR, cadence, elevation)

## Capabilities

### Modified Capabilities
- `activity-time-series-charts`: Updated expanded chart rendering requirements — larger canvas height, wider X-axis tick spacing, larger modal panel

## Impact

- **Frontend JS**: `static/index.html` — `drawTimeSeriesChartExpanded` function (X-axis interval logic)
- **CSS**: `static/css/style.css` — canvas height and modal max-width
