## ADDED Requirements

### Requirement: Climb segment detection
The system SHALL detect climb segments using UCI rules: windowed-difference (5-point window) gradient calculation, merging adjacent segments within 100m, filtering segments < 500m.

#### Scenario: Climb detected on hilly route
- **WHEN** a route with a sustained ≥ 3% gradient over ≥ 500m is processed
- **THEN** that section is identified as a climb with average gradient, distance, and elevation gain

#### Scenario: Flat route yields no climbs
- **WHEN** all sections of a route have gradient < 3%
- **THEN** no climb segments are detected and no climb button is shown

### Requirement: Climb map overlay
Detected climb segments SHALL render as colored Polyline overlays (8px width) on the map: green (<3%), yellow (3-6%), orange (6-9%), red (9-12%), deep red (>12%).

### Requirement: Climb sidebar
A slide-out sidebar SHALL show detailed climb info with left/right navigation. It SHALL display: segment index ("第 X 个 / 共 Y 个"), difficulty level, average gradient, distance, elevation gain, and a segment elevation chart with gradient color coding.

#### Scenario: Sidebar navigation
- **WHEN** user clicks the climb button and then left/right arrows
- **THEN** the sidebar content updates to show the selected climb's details and chart

### Requirement: Climb difficulty classification
Climb segments SHALL be classified as 4级, 3级, 2级, 1级, or HC级 based on UCI categorization of average gradient and total ascent.
