## ADDED Requirements

### Requirement: UCI climb qualification criteria
The system SHALL only classify a climb segment if it meets UCI minimum requirements: length ≥ 1000 meters AND average gradient ≥ 1.3%.

#### Scenario: Segment meets UCI minimums
- **WHEN** a climb segment has length ≥ 1000m and average gradient ≥ 1.3%
- **THEN** the system SHALL assign a UCI category based on the scoring formula

#### Scenario: Segment too short
- **WHEN** a climb segment has length < 1000m
- **THEN** the system SHALL NOT classify it (no difficulty level assigned)

#### Scenario: Segment too shallow
- **WHEN** a climb segment has average gradient < 1.3%
- **THEN** the system SHALL NOT classify it

### Requirement: UCI scoring formula
The system SHALL calculate the UCI climb score as: `Score = Length(km) × Average_Grade(%)²`.

#### Scenario: Score calculation
- **WHEN** a climb segment has length 5000m (5km) and average gradient 8%
- **THEN** the UCI Score SHALL be `5 × 8² = 320`

### Requirement: UCI category thresholds
The system SHALL classify climbs into 5 UCI categories based on score ranges:

| Level | Label | UCI Score Range |
|-------|-------|-----------------|
| 1 | 4级 | 20 – 79 |
| 2 | 3级 | 80 – 199 |
| 3 | 2级 | 200 – 399 |
| 4 | 1级 | 400 – 600 |
| 5 | HC级 | > 600 |

#### Scenario: Category 4 climb (easiest)
- **WHEN** UCI Score is between 20 and 59 (e.g., 2km @ 5% = 50)
- **THEN** the segment SHALL be classified as level 1 with label "4级"

#### Scenario: HC climb (hardest)
- **WHEN** UCI Score exceeds 600 (e.g., 10km @ 8% = 640)
- **THEN** the segment SHALL be classified as level 5 with label "HC级"

#### Scenario: Below minimum score
- **WHEN** UCI Score is below 20 even if length ≥ 1000m and grade ≥ 1.3%
- **THEN** the system SHALL NOT classify it (below UCI 4级 threshold)
