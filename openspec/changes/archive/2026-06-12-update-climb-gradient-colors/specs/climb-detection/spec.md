## MODIFIED Requirements

### Requirement: Color-coded climb visualization on map
The frontend SHALL render climb segments on the map as color-coded polylines matching the unified climb gradient color scheme.

#### Scenario: Climb segments rendered on map
- **WHEN** climb segments data is available
- **THEN** the frontend SHALL overlay polylines on the map for each climb segment
- **AND** use color mapping: level 1 (<3%, #D8F5A2), level 2 (3-6%, #F5BF2A), level 3 (6-9%, #F98925), level 4 (9-12%, #EE3E3E), level 5 (>12%, #B10D0D)

### Requirement: Elevation chart with gradient-colored climbs
The frontend SHALL render the elevation profile chart with climb segments highlighted in gradient-appropriate colors according to the unified color scheme.

#### Scenario: Elevation chart renders climb segments
- **WHEN** elevation data with climb segments is available
- **THEN** the elevation canvas SHALL fill climb segment areas with color corresponding to local gradient
- **AND** the fill color SHALL transition from #D8F5A2 (<3%) through #F5BF2A (3-6%), #F98925 (6-9%), #EE3E3E (9-12%) to #B10D0D (>12%)
