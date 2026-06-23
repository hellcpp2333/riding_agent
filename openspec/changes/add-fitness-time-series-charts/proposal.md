## Why

The activity detail page currently only shows a power-time curve chart. FIT files contain rich sensor data (speed, heart rate, cadence, altitude) that riders expect to see as per-device time-series charts, following the Garmin Connect layout convention. Users need these visualizations to analyze their ride performance holistically across all available data channels.

## What Changes

- Extend the `PowerProfilePoint` schema (rename to generic `ActivityProfilePoint`) to carry `speed`, `cadence`, and `altitude` fields alongside existing `power` and `hr`
- Add four new canvas-based time-series chart sections to the activity detail page: speed-time, heart rate-time, cadence-time, and elevation-time
- Add corresponding expanded modal views for each new chart type
- Charts appear in Garmin Connect order: Power → Speed → Heart Rate → Cadence → Elevation
- Each chart section is conditionally displayed — hidden entirely when the corresponding track data is absent (e.g., no cadence sensor → no cadence chart)
- Uses distinct line/fill colors per chart type matching Garmin's visual language

## Capabilities

### New Capabilities
- `activity-time-series-charts`: Multi-channel time-series chart rendering (speed, heart rate, cadence, elevation) on the activity detail page, with conditional display based on data availability, per-chart expand modals, and Garmin-consistent visual styling.

### Modified Capabilities
<!-- None — this is a pure addition; existing power chart behavior is preserved. -->

## Impact

- **Backend**: `app/api/v1/schemas.py` (`PowerProfilePoint` → add new optional fields), `app/api/v1/activity_routes.py` (`get_activity` profile_points construction — include speed/cadence/altitude)
- **Frontend**: `static/index.html` (new chart canvases in activity detail template, new drawing functions, new modal sections, variable declarations)
- **CSS**: `static/css/style.css` (chart expand button already exists generically; may need minor additions for stacked chart layouts)
- **No dependency changes**, no database migration, no API contract break (all new fields are optional)
