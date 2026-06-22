## MODIFIED Requirements

### Requirement: Power chart X-axis uses time with Garmin HH:MM:SS format
The power profile chart X-axis SHALL display elapsed time formatted as H:MM:SS when total duration ≥ 1 hour, or MM:SS when < 1 hour.

#### Scenario: Ride duration is 2 hours 15 minutes
- **WHEN** the total activity duration is ≥ 1 hour
- **THEN** X-axis labels SHALL use H:MM:SS format (e.g., "0:00:00", "0:30:00", "1:00:00")

#### Scenario: Ride duration is 45 minutes
- **WHEN** the total activity duration is < 1 hour
- **THEN** X-axis labels SHALL use MM:SS format (e.g., "0:00", "15:00", "30:00", "45:00")
