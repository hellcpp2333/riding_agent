## ADDED Requirements

### Requirement: Layout with elevation panel
The map container SHALL be split into a 3:1 flex ratio, with the map area occupying the upper 75% and the elevation data panel occupying the lower 25%.

#### Scenario: Panel visible after route planning
- **WHEN** a route is planned and displayed on the map
- **THEN** the elevation data panel is visible below the map, showing stats cards and an elevation chart placeholder

### Requirement: Route stats cards
The elevation panel SHALL display three horizontally-arranged stat cards in its upper 1/5 area showing distance (km), total ascent (m), and total descent (m), each with a numeric value and Chinese label.

#### Scenario: Stats update with elevation data
- **WHEN** elevation data is received via SSE
- **THEN** the distance card displays the total route distance in kilometers with 1 decimal place, and the ascent/descent cards display values in meters as integers

### Requirement: Elevation profile chart
The elevation panel SHALL render a filled-area elevation profile chart in its lower 4/5 area using Canvas, with elevation (m) on the Y-axis and distance (km) on the X-axis. The chart SHALL use a semi-transparent gradient fill with no line stroke, and SHALL downsample to 300 points for performance.

#### Scenario: Chart renders with data
- **WHEN** elevation trajectory data with at least 2 points is available
- **THEN** a Canvas chart renders showing the elevation profile with grid lines, axis labels, and a filled area under the elevation curve

#### Scenario: Placeholder shown without data
- **WHEN** no elevation data is available
- **THEN** a placeholder message "规划路线后将显示海拔剖面图" is displayed in the chart area
