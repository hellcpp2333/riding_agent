## MODIFIED Requirements

### Requirement: Fine-grained elevation sampling for planned routes
When the agent plans a cycling route via `map_directions`, the system SHALL sample route coordinates at 15-meter intervals and query elevation using the local SRTM DEM provider (primary) or Open Elevation API (fallback).

#### Scenario: Route planning triggers elevation enrichment
- **WHEN** agent calls `map_directions` and route coordinates are extracted
- **THEN** the system SHALL sample coordinates at 15m intervals using Haversine distance
- **AND** convert BD-09 coordinates to WGS-84
- **AND** query elevation via local SRTM DEM provider (without batching limits)
- **AND** fall back to Open Elevation API only if local DEM tiles are unavailable

### Requirement: Elevation stats with 1m climbing threshold
The system SHALL calculate cumulative elevation gain and loss using a 1-meter minimum threshold and Douglas-Peucker smoothing (epsilon=3m) instead of moving average.

#### Scenario: Elevation stats calculation
- **WHEN** elevation data is available for all sample points
- **THEN** the system SHALL apply Douglas-Peucker simplification with epsilon=3m
- **AND** accumulate positive elevation differences > 1m as gain
- **AND** accumulate negative elevation differences < -1m as loss
- **AND** include `stats` (gain, loss, max, min) in the `[ELEVATION_JSON]` block

### Requirement: Elevation enrichment for imported routes
When a user views an imported GPX route detail, the system SHALL return complete elevation profile data. GPX points with embedded elevation SHALL NOT be smoothed (preserving device barometric altimeter accuracy).

#### Scenario: GPX file has embedded elevation data
- **WHEN** user requests GET /api/routes/{id} and the GPX file contains `<ele>` elements
- **THEN** the response SHALL include an `elevation` field with original (unsmoothed) elevation points and cumulative distance
- **AND** the `stats` SHALL be calculated directly from original elevations with 1m threshold

#### Scenario: GPX file lacks elevation data
- **WHEN** user requests GET /api/routes/{id} and the GPX file does NOT contain `<ele>` elements
- **THEN** the system SHALL query local SRTM DEM with the route coordinates (15m sampling for large files)
- **AND** return enriched elevation with Douglas-Peucker smoothing
