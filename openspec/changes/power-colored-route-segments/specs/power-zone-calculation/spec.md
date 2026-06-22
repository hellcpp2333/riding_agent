## ADDED Requirements

### Requirement: Power zone classification for track points
The system SHALL classify each track data point into one of 7 power zones based on the rider's FTP using the Coggan power zone model.

| Zone | Name | %FTP Range |
|------|------|------------|
| Z1 | Active Recovery | 0-55% |
| Z2 | Endurance | 55-75% |
| Z3 | Tempo | 75-90% |
| Z4 | Threshold | 90-105% |
| Z5 | VO2Max | 105-120% |
| Z6 | Anaerobic | 120-150% |
| Z7 | Neuromuscular | >150% |
| Z0 | No Data | power is null or 0 |

#### Scenario: Track point with valid power and known FTP
- **WHEN** a track point has a power value of 200W and the rider's FTP is 220W (90.9% FTP)
- **THEN** the point SHALL be classified as Zone 4 (Threshold, 90-105%)

#### Scenario: Track point power is null or zero
- **WHEN** a track point has power value of null or 0
- **THEN** the point SHALL be classified as Zone 0 (No Data)

#### Scenario: FTP is unavailable (use default)
- **WHEN** the rider's FTP cannot be determined from any activity
- **THEN** the system SHALL use a default FTP of 200W for zone classification

### Requirement: Power segment aggregation
The system SHALL aggregate consecutive track points with the same power zone into power segments with metadata.

#### Scenario: Consecutive points in same zone form a segment
- **WHEN** 50 consecutive track points are all in Zone 3 (Tempo)
- **THEN** the system SHALL produce a single power segment with `start_idx` pointing to the first point, `end_idx` pointing to the last point, `zone` = 3, and `avg_power` = the arithmetic mean of all points' power values

#### Scenario: Zone change creates new segment
- **WHEN** a track point at index N is in Zone 2 but the next point at index N+1 is in Zone 4
- **THEN** the system SHALL close the Zone 2 segment at index N and start a new Zone 4 segment at index N+1

#### Scenario: Isolated Zone 0 points are filtered
- **WHEN** fewer than 3 consecutive points are classified as Zone 0
- **THEN** those points SHALL be merged into the adjacent non-Z0 segment (preferring the preceding segment)

#### Scenario: Minimum segment size enforcement
- **WHEN** a power segment contains fewer than 5 track points
- **THEN** the system SHALL merge it into the preceding segment (or the following segment if no preceding exists)

### Requirement: Power segments in activity API response
The activity detail API endpoint SHALL include power segment data when power data is available in the activity's track data.

#### Scenario: Activity has power data
- **WHEN** a user requests activity details for an activity that contains track points with valid power data
- **THEN** the API response SHALL include a `power_segments` array with each segment containing `start_idx`, `end_idx`, `zone`, and `avg_power`

#### Scenario: Activity has no power data
- **WHEN** a user requests activity details for an activity without power data in track points
- **THEN** the API response SHALL include `power_segments` as null or an empty array
- **AND** the frontend SHALL fall back to single-color route rendering
