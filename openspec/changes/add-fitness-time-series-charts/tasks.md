## 1. Backend schema extension

- [x] 1.1 Add `speed`, `cadence`, `altitude` optional fields to `PowerProfilePoint` in `app/api/v1/schemas.py`

## 2. Backend endpoint update

- [x] 2.1 Include `speed`, `cadence`, `altitude` in profile_points construction within `GET /api/activities/{id}` in `app/api/v1/activity_routes.py`

## 3. Frontend shared chart utility

- [x] 3.1 Create `drawTimeSeriesChart(canvasId, data, options)` shared canvas drawing function that accepts per-chart config (valueKey, lineColor, fillColor, unit, avgFormatter) and renders the same pattern as the existing power chart (grid, axes, trace line, gradient fill, average dashed line)

## 4. Frontend chart rendering functions

- [x] 4.1 Implement `drawSpeedChart(data)` calling shared utility with speed config (blue #2e86de, km/h)
- [x] 4.2 Implement `drawHrChart(data)` calling shared utility with HR config (red #e74c3c, bpm)
- [x] 4.3 Implement `drawCadenceChart(data)` calling shared utility with cadence config (green #2ecc71, rpm)
- [x] 4.4 Implement `drawElevationChart(data)` calling shared utility with elevation config (purple #8e44ad, m)
- [x] 4.5 Refactor existing `drawPowerProfileChart` to use the shared utility

## 5. Frontend activity detail template

- [x] 5.1 Add speed-time chart section with canvas (`#speed-canvas`), title, expand button, conditional `v-if` display based on `hasSpeed` computed property
- [x] 5.2 Add heart rate-time chart section with canvas (`#hr-time-canvas`), title, expand button, conditional `v-if` display based on `hasHrTime` computed property
- [x] 5.3 Add cadence-time chart section with canvas (`#cadence-canvas`), title, expand button, conditional `v-if` display based on `hasCadence` computed property
- [x] 5.4 Add elevation-time chart section with canvas (`#elevation-canvas`), title, expand button, conditional `v-if` display based on `hasAltitude` computed property
- [x] 5.5 Ensure chart sections follow Garmin order: Power → Speed → Heart Rate → Cadence → Elevation

## 6. Frontend expand modals

- [x] 6.1 Add speed chart expand modal with `#speed-canvas-expanded` canvas
- [x] 6.2 Add heart rate chart expand modal with `#hr-time-canvas-expanded` canvas
- [x] 6.3 Add cadence chart expand modal with `#cadence-canvas-expanded` canvas
- [x] 6.4 Add elevation chart expand modal with `#elevation-canvas-expanded` canvas
- [x] 6.5 Implement per-chart `open*Modal`/`close*Modal` handler functions and expanded draw functions

## 7. Frontend data detection and reactivity

- [x] 7.1 Add computed properties: `hasPowerData`, `hasSpeed`, `hasHrTime`, `hasCadence`, `hasAltitude` checking profile array for valid data
- [x] 7.2 Wire `selectActivity` → after API response, call `drawSpeedChart`, `drawHrChart`, `drawCadenceChart`, `drawElevationChart` via `nextTick`

## 8. CSS adjustments

- [x] 8.1 Add canvas sizing styles for new chart canvases (same 220px height as power chart)
- [x] 8.2 Add expanded canvas sizing styles for new modal canvases (same 480px height)

## 9. Verification

- [ ] 9.1 Test with FIT file containing all sensors — verify all 5 charts render in correct order
- [ ] 9.2 Test with FIT file missing cadence — verify cadence chart is hidden, others show
- [ ] 9.3 Test each chart's expand button — verify modal opens with correct expanded chart
- [ ] 9.4 Test backward compatibility — verify existing activity (pre-change) still shows power chart only
