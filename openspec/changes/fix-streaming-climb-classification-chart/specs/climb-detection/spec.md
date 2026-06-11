## MODIFIED Requirements

### Requirement: Automatic climb segment detection
The system SHALL automatically detect climb segments from elevation data using a sliding window gradient analysis, with a minimum segment length of 1000 meters and minimum average gradient of 1.3%, per UCI standards.

#### Scenario: Route contains a sustained climb
- **WHEN** elevation data shows a gradient ≥ 3% sustained over ≥ 1000 meters
- **THEN** the system SHALL identify it as a climb segment
- **AND** record start index, end index, average gradient, distance, and elevation gain

#### Scenario: Route contains no significant climb
- **WHEN** no segment meets the 1.3% / 1000m criteria
- **THEN** the system SHALL return an empty climb segments array
- **AND** the frontend SHALL hide the climb list and climb sidebar

### Requirement: Five-level climb classification (UCI standard)
The system SHALL classify each detected climb segment using the UCI scoring formula: `Score = Length(km) × Average_Grade(%)²`, with the following thresholds:

| Level | Label | UCI Score Range |
|-------|-------|-----------------|
| 1 | 4级 | 20 – 79 |
| 2 | 3级 | 80 – 199 |
| 3 | 2级 | 200 – 399 |
| 4 | 1级 | 400 – 600 |
| 5 | HC级 | > 600 |

Segments with score < 20 SHALL NOT be classified.

#### Scenario: HC climb classification (UCI)
- **WHEN** a climb segment has UCI Score > 600 (e.g., 10km @ 8% = 640)
- **THEN** the segment SHALL be classified as difficulty level 5 with label "HC级"

#### Scenario: Category 4 climb classification (UCI)
- **WHEN** a climb segment has UCI Score between 20 and 59 (e.g., 2km @ 5% = 50)
- **THEN** the segment SHALL be classified as difficulty level 1 with label "4级"
