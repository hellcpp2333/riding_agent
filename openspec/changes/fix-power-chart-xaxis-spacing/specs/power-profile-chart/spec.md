## MODIFIED Requirements

### Requirement: X-axis label spacing prevents overlap
The power chart X-axis SHALL use larger tick intervals to prevent label overlap.

#### Scenario: 2-hour ride in mini chart
- **WHEN** total duration is 2 hours
- **THEN** X-axis ticks SHALL appear at 15-minute intervals (max 9 labels)

#### Scenario: 2-hour ride in expanded chart
- **WHEN** expanded modal is open for a 2-hour ride
- **THEN** X-axis ticks SHALL appear at 10-minute intervals on a 1400px-wide chart
