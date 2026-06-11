## ADDED Requirements

### Requirement: Conditional panel visibility
The elevation data panel and climb segment button SHALL be hidden when no route is displayed on the map, and SHALL appear when elevation data is received.

#### Scenario: Panel hidden initially
- **WHEN** the page loads and no route has been planned
- **THEN** the elevation data panel is not visible and the map occupies the full height of the map container

#### Scenario: Panel appears with route
- **WHEN** a route is planned and elevation data is received via SSE
- **THEN** the elevation panel and climb button become visible, and the map area smoothly transitions to 75% height

#### Scenario: Panel hides when route cleared
- **WHEN** the map is cleared (via `clearMap()` or new session)
- **THEN** the elevation panel and climb button are hidden, and the map returns to full height

### Requirement: Layout with elevation panel
The map container SHALL split into a 3:1 flex ratio when a route is present, with the map area occupying 75% and the elevation panel 25%.

### Requirement: Route stats cards
The elevation panel SHALL display three horizontally-arranged stat cards: distance (km, 1 decimal), total ascent (m, integer), and total descent (m, integer), each with a value above a Chinese label.

#### Scenario: Stats display elevation data
- **WHEN** elevation data with cumulative distance and elevation values is available
- **THEN** the three cards show the computed distance, ascent, and descent

### Requirement: Elevation profile chart
The elevation panel SHALL render a filled-area elevation profile chart using Canvas in the lower 4/5 of the panel, with elevation (m) on Y-axis and distance (km) on X-axis, downsampled to 300 points.

#### Scenario: Chart renders elevation profile
- **WHEN** elevation trajectory data with ≥ 2 points is available
- **THEN** a Canvas chart renders with grid lines, axis labels, and a semi-transparent gradient-filled area under the elevation curve with no line stroke
