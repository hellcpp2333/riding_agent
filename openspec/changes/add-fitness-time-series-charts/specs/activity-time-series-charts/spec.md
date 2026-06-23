## ADDED Requirements

### Requirement: Extended profile point schema

The `PowerProfilePoint` schema SHALL include optional `speed` (float km/h), `cadence` (int rpm), and `altitude` (float m) fields alongside existing `time_sec`, `dist_km`, `power`, and `hr` fields.

#### Scenario: Full sensor data present
- **WHEN** a FIT file contains speed, cadence, and altitude records
- **THEN** the API response profile points SHALL include non-null values for `speed`, `cadence`, and `altitude`

#### Scenario: Partial sensor data
- **WHEN** a FIT file lacks cadence data (no cadence sensor)
- **THEN** the API response profile points SHALL have `cadence` set to `null`

#### Scenario: Legacy track data without new fields
- **WHEN** track data JSON on OSS was stored before this change and lacks `speed`/`cadence`/`altitude` keys
- **THEN** the API response profile points SHALL have those fields as `null`

### Requirement: Speed-time curve chart

The system SHALL render a speed-time curve chart on the activity detail page when speed data is present in the profile points.

#### Scenario: Speed data available
- **WHEN** activity detail loads and at least one profile point has `speed > 0`
- **THEN** a canvas chart with speed (km/h) on Y-axis and time on X-axis SHALL be displayed
- **THEN** the chart SHALL show a blue (#2e86de) speed trace line with gradient fill, an average speed dashed line, and labeled axes

#### Scenario: No speed data
- **WHEN** activity detail loads and no profile point has valid `speed` data
- **THEN** the speed-time chart section SHALL be hidden

### Requirement: Heart rate-time curve chart

The system SHALL render a heart rate-time curve chart on the activity detail page when heart rate data is present.

#### Scenario: Heart rate data available
- **WHEN** activity detail loads and at least one profile point has `hr > 0`
- **THEN** a canvas chart with heart rate (bpm) on Y-axis and time on X-axis SHALL be displayed
- **THEN** the chart SHALL show a red (#e74c3c) HR trace line with gradient fill, an average HR dashed line, and labeled axes

#### Scenario: No heart rate data
- **WHEN** activity detail loads and no profile point has valid `hr` data
- **THEN** the heart rate-time chart section SHALL be hidden

### Requirement: Cadence-time curve chart

The system SHALL render a cadence-time curve chart on the activity detail page when cadence data is present.

#### Scenario: Cadence data available
- **WHEN** activity detail loads and at least one profile point has `cadence > 0`
- **THEN** a canvas chart with cadence (rpm) on Y-axis and time on X-axis SHALL be displayed
- **THEN** the chart SHALL show a green (#2ecc71) cadence trace line with gradient fill, an average cadence dashed line, and labeled axes

#### Scenario: No cadence data
- **WHEN** activity detail loads and no profile point has valid `cadence` data
- **THEN** the cadence-time chart section SHALL be hidden

### Requirement: Elevation-time curve chart

The system SHALL render an elevation-time curve chart on the activity detail page when altitude data is present in the profile points.

#### Scenario: Elevation data available
- **WHEN** activity detail loads and at least one profile point has non-null `altitude`
- **THEN** a canvas chart with elevation (m) on Y-axis and time on X-axis SHALL be displayed
- **THEN** the chart SHALL show a purple (#8e44ad) elevation trace line with gradient fill and labeled axes

#### Scenario: No elevation data
- **WHEN** activity detail loads and no profile point has valid `altitude` data
- **THEN** the elevation-time chart section SHALL be hidden

### Requirement: Garmin chart ordering

The activity detail page SHALL display time-series charts in the following top-to-bottom order: Power → Speed → Heart Rate → Cadence → Elevation.

#### Scenario: All charts present
- **WHEN** all five data channels (power, speed, heart rate, cadence, elevation) have data
- **THEN** charts SHALL appear in the fixed order: Power, Speed, Heart Rate, Cadence, Elevation

#### Scenario: Partial charts present
- **WHEN** only power, heart rate, and elevation have data
- **THEN** charts SHALL appear in the order: Power, Heart Rate, Elevation (gaps removed, relative order preserved)

### Requirement: Per-chart expand modal

Each time-series chart SHALL have an expand button that opens a full-width modal with a larger rendering of the same chart.

#### Scenario: Expand speed chart
- **WHEN** user clicks the expand button on the speed-time chart
- **THEN** a modal overlay SHALL open with a full-width speed-time chart (canvas height ≥ 400px)
- **THEN** clicking the close button or backdrop SHALL close the modal

#### Scenario: Expand heart rate chart
- **WHEN** user clicks the expand button on the heart rate-time chart
- **THEN** a modal overlay SHALL open with a full-width heart rate-time chart

### Requirement: Shared chart rendering utility

The implementation SHALL use a shared canvas drawing function to avoid code duplication across chart types.

#### Scenario: Consistent chart appearance
- **WHEN** any time-series chart is rendered
- **THEN** it SHALL use the same axis styling, grid line pattern, font sizes, and padding as the existing power chart
- **THEN** only the data field, line color, fill gradient colors, unit label, and average value formatter SHALL differ between chart types
