## ADDED Requirements

### Requirement: Fine-grained elevation sampling for planned routes
When the agent plans a cycling route via `map_directions`, the system SHALL sample route coordinates at 30-meter intervals and query elevation from Open Elevation API for each sample point.

#### Scenario: Route planning triggers elevation enrichment
- **WHEN** agent calls `map_directions` and route coordinates are extracted
- **THEN** the system SHALL sample coordinates at 30m (±5m) intervals using Haversine distance
- **AND** convert BD-09 coordinates to WGS-84
- **AND** batch-query Open Elevation API (max 800 points per request)
- **AND** return elevation data for all sampled points

#### Scenario: Long routes require multiple API batches
- **WHEN** a route exceeds ~24km (more than 800 sampled points)
- **THEN** the system SHALL split points into batches of 800 and issue multiple API requests sequentially
- **AND** merge results into a single elevation dataset

### Requirement: Elevation stats with 3m climbing threshold
The system SHALL calculate cumulative elevation gain and loss using a 3-meter minimum threshold and 3-point moving average smoothing.

#### Scenario: Elevation stats calculation
- **WHEN** elevation data is available for all sample points
- **THEN** the system SHALL apply 3-point moving average smoothing
- **AND** accumulate positive elevation differences > 3m as gain
- **AND** accumulate negative elevation differences < -3m as loss
- **AND** include `stats` (gain, loss, max, min) in the `[ELEVATION_JSON]` block

### Requirement: Elevation enrichment for imported routes
When a user views an imported GPX route detail, the system SHALL return complete elevation profile data including per-point elevation and cumulative distance.

#### Scenario: GPX file has embedded elevation data
- **WHEN** user requests GET /api/routes/{id} and the GPX file contains `<ele>` elements
- **THEN** the response SHALL include an `elevation` field with `points` (lat, lon, ele, dist) and `stats` (gain, loss, max, min)
- **AND** the frontend SHALL render the elevation profile panel using this data

#### Scenario: GPX file lacks elevation data
- **WHEN** user requests GET /api/routes/{id} and the GPX file does NOT contain `<ele>` elements
- **THEN** the system SHALL query Open Elevation API with the route coordinates (30m sampling)
- **AND** return the enriched elevation data in the response

### Requirement: Client-side uses backend-computed elevation stats
The frontend SHALL use elevation stats from the backend `[ELEVATION_JSON]` data directly, without recalculating gain/loss locally.

#### Scenario: Elevation panel displays backend stats
- **WHEN** frontend receives an `elevation` event via SSE or from route detail API
- **THEN** the stats panel SHALL display gain, loss, max, and min values directly from `data.stats`
- **AND** the frontend SHALL NOT recalculate these values with its own threshold
