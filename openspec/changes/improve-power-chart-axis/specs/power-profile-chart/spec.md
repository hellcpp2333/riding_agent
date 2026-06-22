## MODIFIED Requirements

### Requirement: Power profile chart replaces power curve
The activity detail panel SHALL display a power-over-distance profile chart with the X-axis showing cumulative distance in kilometers, following Garmin Connect's chart axis convention.

#### Scenario: Activity has power data in track records
- **WHEN** a user views an activity detail that has power data in its track records
- **THEN** the chart title SHALL read "功率曲线"
- **AND** the X-axis SHALL represent cumulative distance in kilometers (km)
- **AND** the Y-axis SHALL represent power in watts (W)
- **AND** the chart SHALL render a line connecting power values across the full activity distance
- **AND** a horizontal dashed line SHALL indicate the average power with a text label showing "平均 xxx W"

#### Scenario: X-axis distance tick spacing (Garmin-style)
- **WHEN** the total activity distance is less than 10 km
- **THEN** X-axis labels SHALL appear at 1 km intervals
- **WHEN** the total distance is between 10 and 50 km
- **THEN** X-axis labels SHALL appear at 5 km intervals
- **WHEN** the total distance exceeds 50 km
- **THEN** X-axis labels SHALL appear at 10 km intervals

#### Scenario: Activity has no power data
- **WHEN** the activity track records contain no power data
- **THEN** the chart section SHALL NOT be displayed

### Requirement: Expanded chart modal dimensions
The expanded power chart modal SHALL render a taller canvas with wider X-axis tick spacing for improved readability.

#### Scenario: Modal chart renders with increased height
- **WHEN** the expanded chart modal is opened
- **THEN** the canvas SHALL have a height of 450px (vs 220px for the mini chart)
- **AND** the X-axis tick spacing SHALL follow the same distance-based interval rules

### Requirement: Power profile data includes distance
The activity detail API SHALL include cumulative distance (`dist_km`) in each `PowerProfilePoint`.

#### Scenario: Activity has power data with valid coordinates
- **WHEN** the backend builds power profile points from track data
- **THEN** each point SHALL include `dist_km: float` representing cumulative distance in kilometers from the first record
