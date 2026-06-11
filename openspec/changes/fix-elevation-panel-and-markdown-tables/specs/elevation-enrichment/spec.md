## MODIFIED Requirements

### Requirement: Elevation stats calculation
The system SHALL compute cumulative distances before applying Douglas-Peucker smoothing when calculating elevation stats, ensuring the `dist` field exists on all points passed to the DP algorithm.

#### Scenario: Route planning elevation flow
- **WHEN** elevation data is returned from local DEM or Open Elevation API (points have lat/lon/ele only)
- **THEN** the system SHALL compute cumulative distances first
- **AND** then apply Douglas-Peucker smoothing on the distance-enriched points
- **AND** then calculate elevation stats from the smoothed points

#### Scenario: GPX route without embedded elevation
- **WHEN** enrich_route_with_elevation is called for a GPX without ele tags
- **THEN** the system SHALL compute cumulative distances on elevation lookup results BEFORE applying DP smoothing
