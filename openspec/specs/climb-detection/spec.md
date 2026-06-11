## ADDED Requirements

### Requirement: Automatic climb segment detection
The system SHALL automatically detect climb segments from elevation data using a sliding window gradient analysis, with a minimum segment length of 300 meters and minimum average gradient of 3%.

#### Scenario: Route contains a sustained climb
- **WHEN** elevation data shows a gradient ≥ 3% sustained over ≥ 300 meters
- **THEN** the system SHALL identify it as a climb segment
- **AND** record start index, end index, average gradient, distance, and elevation gain

#### Scenario: Route contains no significant climb
- **WHEN** no segment meets the 3% / 300m criteria
- **THEN** the system SHALL return an empty climb segments array
- **AND** the frontend SHALL hide the climb list and climb sidebar

### Requirement: Five-level climb classification (Garmin-style)
The system SHALL classify each detected climb segment into one of 5 difficulty levels following Garmin Connect's classification scheme.

| Level | Label | Criteria |
|-------|-------|----------|
| 5 | HC级 | avgGrade ≥ 8% OR elevationGain ≥ 800m |
| 4 | 1级 | avgGrade ≥ 6% OR elevationGain ≥ 500m |
| 3 | 2级 | avgGrade ≥ 5% OR elevationGain ≥ 300m |
| 2 | 3级 | avgGrade ≥ 4% OR elevationGain ≥ 150m |
| 1 | 4级 | avgGrade ≥ 3% OR elevationGain ≥ 75m |

#### Scenario: HC climb classification
- **WHEN** a climb segment has average gradient ≥ 8% or elevation gain ≥ 800m
- **THEN** the segment SHALL be classified as difficulty level 5 with label "HC级"

#### Scenario: Category 4 climb classification
- **WHEN** a climb segment has average gradient ≥ 3%, gain ≥ 75m, and does NOT meet higher category criteria
- **THEN** the segment SHALL be classified as difficulty level 1 with label "4级"

### Requirement: Climb data included in elevation JSON
The system SHALL include detected climb segments in the `[ELEVATION_JSON]` block alongside elevation points and stats.

#### Scenario: Elevation JSON includes climbs
- **WHEN** elevation data is available and climbs are detected
- **THEN** the `[ELEVATION_JSON]` block SHALL contain a `climbs` array with each segment's startIdx, endIdx, avgGrade, distance, elevationGain, difficulty, and difficultyLabel
- **AND** the frontend SHALL parse this array and render the climb list and map overlays

### Requirement: Color-coded climb visualization on map
The frontend SHALL render climb segments on the map as color-coded polylines matching Garmin's gradient color scheme.

#### Scenario: Climb segments rendered on map
- **WHEN** climb segments data is available
- **THEN** the frontend SHALL overlay polylines on the map for each climb segment
- **AND** use color mapping: level 1 (green #4caf50), level 2 (yellow #fdd835), level 3 (orange #ff9800), level 4 (red #e53935), level 5 (dark red #880e0e)

### Requirement: Elevation chart with gradient-colored climbs
The frontend SHALL render the elevation profile chart with climb segments highlighted in gradient-appropriate colors, following Garmin's visualization style.

#### Scenario: Elevation chart renders climb segments
- **WHEN** elevation data with climb segments is available
- **THEN** the elevation canvas SHALL fill climb segment areas with intensity proportional to local gradient
- **AND** the fill color SHALL transition from green (<3%) through yellow-orange-red to dark red (>12%)
