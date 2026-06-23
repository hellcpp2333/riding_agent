## MODIFIED Requirements

### Requirement: Per-chart expand modal

Each time-series chart SHALL have an expand button that opens a full-width modal with a larger rendering of the same chart. The expanded canvas height SHALL be 600px. The modal panel SHALL have max-width 1600px. The X-axis SHALL use time tick intervals of at least 5 minutes, with wider intervals for longer rides (10min for >1h, 15min for >2h, 20min for >4h).

#### Scenario: Expand speed chart
- **WHEN** user clicks the expand button on the speed-time chart
- **THEN** a modal overlay SHALL open with a full-width speed-time chart (canvas height 600px)
- **THEN** X-axis time ticks SHALL be spaced at ≥5 minute intervals
- **THEN** clicking the close button or backdrop SHALL close the modal

#### Scenario: Expand cadence chart
- **WHEN** user clicks the expand button on the cadence-time chart  
- **THEN** a modal overlay SHALL open with a full-width cadence-time chart (canvas height 600px)
- **THEN** X-axis time ticks SHALL be spaced at ≥5 minute intervals

#### Scenario: Short ride X-axis spacing
- **WHEN** expanded chart renders for a ride ≤30 minutes
- **THEN** X-axis SHALL use 5-minute tick intervals
