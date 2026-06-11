## ADDED Requirements

### Requirement: Climb chart axis labels
The climb segment elevation chart SHALL display Y-axis elevation labels (meters) and X-axis distance labels (kilometers) with axis titles.

#### Scenario: Climb chart renders with axes
- **WHEN** the climb sidebar is opened for a climb segment
- **THEN** the chart SHALL display 3-4 Y-axis tick marks labeled with elevation values in meters
- **AND** display 3-4 X-axis tick marks labeled with distance values in kilometers
- **AND** display "距离 (km)" axis title and "海拔 (m)" axis title

### Requirement: Main elevation chart Garmin green color
The main elevation profile chart SHALL use a green color scheme matching Garmin's visualization, replacing the current blue gradient.

#### Scenario: Main chart green fill
- **WHEN** the elevation profile chart is drawn
- **THEN** the filled area SHALL use a green gradient from `rgba(76,175,80,0.45)` at top to `rgba(200,230,201,0.02)` at bottom
- **AND** the curve stroke SHALL be `#66bb6a` (medium green)

### Requirement: Gradient legend spans chart width
The climb gradient legend SHALL span from the left edge to the right edge of the chart above it, with color indicators evenly distributed.

#### Scenario: Legend aligned with chart
- **WHEN** climb chart renders with a specific width
- **THEN** the gradient legend below it SHALL use `justify-content: space-between` to fill the same horizontal space
- **AND** color indicators SHALL be evenly spaced from left to right
