## ADDED Requirements

### Requirement: Climb segment detection
The system SHALL detect climb segments along a route based on UCI rules: a windowed-difference calculation identifies sections with average gradient ≥ 3%, and adjacent sections within 100m are merged. Only segments with total length ≥ 500m are retained.

#### Scenario: Climb detected on hilly route
- **WHEN** a route with elevation points containing a sustained 5% gradient over 2km is processed
- **THEN** that section is identified as a climb segment with its average gradient, total distance, and elevation gain calculated

#### Scenario: Flat route has no climbs
- **WHEN** a route where all sections have gradient < 3% is processed
- **THEN** no climb segments are detected

### Requirement: Climb segments on map
Detected climb segments SHALL be rendered on the map as colored polyline overlays atop the base route, using gradient-based colors: green (<3%), yellow (3-6%), orange (6-9%), red (9-12%), deep red (>12%).

#### Scenario: Multi-color climb rendering
- **WHEN** a route has climb segments of varying gradients
- **THEN** each segment is rendered with the appropriate color on the map, visually distinguishable from the base route

### Requirement: Climb sidebar
A slide-out sidebar SHALL display detailed information for each climb segment. The sidebar SHALL include navigation arrows to switch between climbs, showing: "第 X 个 / 共 Y 个", difficulty level, average gradient, distance, and elevation gain. The sidebar SHALL also render a segment-specific elevation chart with gradient-based color coding.

#### Scenario: Sidebar opens with climb details
- **WHEN** the user clicks the "爬坡段" button after climb segments are detected
- **THEN** the sidebar slides in from the right, showing the first climb's details and gradient-colored elevation chart

#### Scenario: Navigate between climbs
- **WHEN** the user clicks the left/right arrow buttons in the sidebar
- **THEN** the displayed climb index updates, and all details and the chart refresh to show the selected climb segment

#### Scenario: Sidebar closes
- **WHEN** the user clicks the close button or overlay backdrop
- **THEN** the sidebar slides out and the overlay fades away

### Requirement: Climb difficulty classification
Climb segments SHALL be classified into difficulty levels based on their characteristics following UCI categorization standards.

#### Scenario: Difficulty levels
- **WHEN** a climb segment is identified
- **THEN** it is classified as one of: 4级 (lowest), 3级, 2级, 1级, or HC级 (highest) based on average gradient and total ascent
