## ADDED Requirements

### Requirement: Power profile chart replaces power curve
The activity detail panel SHALL display a power-over-time profile chart (功率曲线剖面图) instead of the power-duration curve (Power Curve), showing the rider's power output throughout the entire activity.

#### Scenario: Activity has power data in track records
- **WHEN** a user views an activity detail that has power data in its track records
- **THEN** the chart title SHALL read "功率曲线"
- **AND** the X-axis SHALL represent cumulative time in MM:SS format
- **AND** the Y-axis SHALL represent power in watts (W)
- **AND** the chart SHALL render a line connecting power values across the full activity duration

#### Scenario: Activity has no power data
- **WHEN** the activity track records contain no power data
- **THEN** the chart section SHALL NOT be displayed

#### Scenario: Track data exceeds rendering threshold
- **WHEN** the power profile data contains more than 1000 data points
- **THEN** the chart SHALL downsample to at most 1000 points using median sampling before rendering

### Requirement: Power profile data in API response
The activity detail API SHALL return a `power_profile` array alongside `track_data` when power data is available.

#### Scenario: Activity has power data
- **WHEN** the activity detail API loads track data that contains power values
- **THEN** the response SHALL include a `power_profile` field containing `[{time_sec: float, power: int, hr: int|null}]` for each record point
- **AND** `time_sec` SHALL be cumulative seconds from the first record

#### Scenario: Activity has no power data
- **WHEN** the activity track data contains no valid power values
- **THEN** `power_profile` SHALL be null or an empty array
- **AND** the frontend SHALL hide the chart section
