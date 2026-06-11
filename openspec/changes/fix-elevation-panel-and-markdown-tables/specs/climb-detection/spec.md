## MODIFIED Requirements

### Requirement: Climb chart gradient legend
The frontend SHALL display a gradient legend below the climb segment elevation chart, showing the color-to-grade mapping following Garmin Connect's visualization standard.

#### Scenario: Climb chart renders with legend
- **WHEN** the climb sidebar is opened and a climb chart is drawn
- **THEN** a horizontal gradient legend SHALL appear below the chart
- **AND** SHALL display 5 grade ranges: <3% (light green), 3-6% (green), 6-9% (orange), 9-12% (yellow), >12% (red)

#### Scenario: Climb sidebar closed
- **WHEN** the climb sidebar is closed
- **THEN** the gradient legend SHALL NOT be visible
