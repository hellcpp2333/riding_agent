## MODIFIED Requirements

### Requirement: Distance marker visual style
Distance markers SHALL display as white filled circles overlaid on the route line, with the distance number rendered in black inside the circle. No text SHALL appear outside the marker.

#### Scenario: Marker appearance
- **WHEN** a distance marker is rendered
- **THEN** a white circle (#fff) of 22px diameter with 1.5px dark gray border is displayed at the marker's coordinate
- **THEN** the distance number in kilometers (integer, no unit suffix) is displayed centered inside the circle in black bold 11px font
- **THEN** no external text label is visible

#### Scenario: Marker occludes route line
- **WHEN** a distance marker is rendered at a position on the route polyline
- **THEN** the white circle fully covers the route line at that position, making the marker clearly visible against the route
