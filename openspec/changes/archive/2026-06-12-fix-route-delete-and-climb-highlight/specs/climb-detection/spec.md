## MODIFIED Requirements

### Requirement: Color-coded climb visualization on map
The frontend SHALL render climb segments on the map as color-coded polylines matching the unified climb gradient color scheme. The currently selected segment SHALL be visually highlighted with full opacity and heavier stroke weight, while non-selected segments SHALL appear at reduced opacity.

#### Scenario: Climb segments rendered on map
- **WHEN** climb segments data is available
- **THEN** the frontend SHALL overlay polylines on the map for each climb segment
- **AND** use color mapping: level 1 (<3%, #D8F5A2), level 2 (3-6%, #F5BF2A), level 3 (6-9%, #F98925), level 4 (9-12%, #EE3E3E), level 5 (>12%, #B10D0D)

#### Scenario: Selected climb segment highlighted on map
- **WHEN** a specific climb segment is selected (via sidebar or list click)
- **THEN** the selected segment polyline SHALL render at strokeOpacity 0.9 and strokeWeight 10
- **AND** non-selected segments SHALL render at strokeOpacity 0.35 and strokeWeight 6
- **AND** the map SHALL pan to center the selected segment
