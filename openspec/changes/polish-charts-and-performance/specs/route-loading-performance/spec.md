## ADDED Requirements

### Requirement: Track data downsampling for display
The system SHALL downsample route track data to a maximum of 500 points before rendering on the map, ensuring smooth performance regardless of route length.

#### Scenario: Long route loaded
- **WHEN** a route with > 500 track points is loaded
- **THEN** the server SHALL return at most 500 evenly-sampled track points
- **AND** the frontend SHALL further downsample if needed before creating map polylines

### Requirement: Canvas render debouncing
The frontend SHALL debounce elevation chart redraws to avoid redundant rendering when switching routes rapidly.

#### Scenario: Rapid route switching
- **WHEN** user clicks multiple routes in quick succession
- **THEN** only the final selected route's elevation chart SHALL be rendered
- **AND** intermediate chart renders SHALL be cancelled via cancelAnimationFrame
