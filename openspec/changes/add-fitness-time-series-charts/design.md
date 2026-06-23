## Context

The activity detail page currently renders a single power-time curve chart using Canvas 2D (`drawPowerProfileChart`). The backend `GET /api/activities/{id}` endpoint returns `power_profile` — an array of `PowerProfilePoint` objects with `time_sec`, `dist_km`, `power`, `hr`. The FIT parser (`fit_service.py`) already extracts `speed`, `cadence`, and `altitude` from FIT records and stores them in track data JSON on OSS.

The refer folder contains Garmin Connect reference HTML showing the chart ordering convention: Power → Speed → Heart Rate → Cadence → Elevation.

## Goals / Non-Goals

**Goals:**
- Add speed-time, heart rate-time, cadence-time, and elevation-time canvas charts to the activity detail page
- Each chart uses the same visual pattern as the existing power chart (line + gradient fill + average dashed line + axis labels)
- Charts appear in Garmin order: Power → Speed → Heart Rate → Cadence → Elevation
- Each chart is hidden entirely when its corresponding track data is absent
- Each chart has a small expand button opening a full-width modal
- Use distinct colors per chart type consistent with Garmin's visual language

**Non-Goals:**
- No change to the power curve algorithm (`build_power_curve` in fit_service)
- No new chart library (Recharts, Chart.js, etc.) — continue using Canvas 2D
- No database schema changes
- No new API endpoints
- No change to the existing power chart except for the surrounding layout

## Decisions

### 1. Extend `PowerProfilePoint` schema (no rename)

The existing `PowerProfilePoint` already carries `hr` alongside `power`. Adding `speed`, `cadence`, and `altitude` as optional fields keeps backward compatibility. Renaming to `ActivityProfilePoint` would be a **BREAKING** change for no benefit — the name is internal to the JSON response and renaming adds risk.

**Alternative considered**: Create separate `SpeedProfilePoint`, `HrProfilePoint` etc. schemas. Rejected: duplicative; all share the same time axis; single array is simpler for the frontend to consume.

### 2. Reuse canvas rendering pattern with parameterized helper

Extract a shared `drawTimeSeriesChart(canvasId, config)` function that accepts per-chart configuration (data field, color, unit label, Y-axis suffix). Each chart calls this helper with its own config. This avoids copy-pasting 4× ~100 lines of canvas code.

**Config shape**: `{ dataField: 'speed'|'hr'|'cadence'|'altitude', lineColor, fillColorTop, fillColorBottom, unitLabel, valueFormatter, hasAverage: bool }`

**Alternative considered**: Copy-paste `drawPowerProfileChart` 4 times with search-and-replace. Rejected: maintenance burden when fixing bugs or adjusting styling.

### 3. Backend: include all fields in profile_points construction

In `GET /api/activities/{id}`, the loop that builds `profile_points` currently reads `power` and `hr` from each track point. Extend it to also read `speed`, `cadence`, and `altitude`. The downsampling logic (median of chunk, max 1000 points) applies uniformly — no per-field special handling needed.

### 4. Conditional display via data availability detection

After receiving the response, the frontend checks:
- `hasSpeed = profile.some(p => p.speed != null && p.speed > 0)`
- `hasHr = profile.some(p => p.hr != null && p.hr > 0)` (already nullable)
- `hasCadence = profile.some(p => p.cadence != null && p.cadence > 0)`
- `hasAltitude = profile.some(p => p.altitude != null)`

These booleans drive `v-if` on each chart section.

**Alternative considered**: Backend sends separate `has_*` flags. Rejected: easy enough to compute client-side from the data that's already present; avoids adding response fields.

### 5. Garmin color mapping

| Chart     | Line Color | Fill Gradient Top         | Unit  |
|-----------|-----------|---------------------------|-------|
| Power     | #ee3e3e   | rgba(238,62,62,0.18)→0.02 | W     |
| Speed     | #2e86de   | rgba(46,134,222,0.18)→0.02| km/h  |
| Heart Rate| #e74c3c   | rgba(231,76,60,0.18)→0.02 | bpm   |
| Cadence   | #2ecc71   | rgba(46,204,113,0.18)→0.02| rpm   |
| Elevation | #8e44ad   | rgba(142,68,173,0.18)→0.02| m     |

These colors approximate Garmin Connect's chart palette.

### 6. Modular drawing functions approach

Rather than one monolithic helper, use a lighter approach: a `drawTimeSeriesChart(canvasId, data, options)` function where `options` provides `{ valueKey, lineColor, fillColor, unit, avgFormatter }`. This keeps each chart call site clean while avoiding a massive abstraction.

## Risks / Trade-offs

- **Page length**: 5 stacked charts (power + 4 new) could make the detail view very long. Mitigation: each chart is only 220px tall (same as current power chart), so 5 charts ≈ 1100px — acceptable for a scrollable detail panel.
- **Canvas rendering performance**: 5 canvas elements each with up to 1000 downsampled points. Mitigation: Canvas 2D handles this trivially; use `requestAnimationFrame` per chart (separate animation frame IDs).
- **No data = no chart**: If a FIT file lacks cadence (common for basic head units), the cadence chart won't render. This is intentional and matches Garmin behavior. The HR chart similarly hides when no HR sensor data exists.
- **Backward compatibility**: Old track data JSON on OSS lacks `speed`/`cadence`/`altitude` fields — these will simply be `None`/`null` and the corresponding charts will hide. No migration needed.

## Open Questions

<!-- None — approach is straightforward. -->
