## MODIFIED Requirements

### Requirement: Distance marker visual style
Distance markers SHALL use a Garmin-style visual design with a filled circular dot and distance text label. The dot SHALL be 14px in diameter to fully cover the route polyline width.

#### Scenario: Marker dot appearance
- **WHEN** a distance marker is rendered
- **THEN** a filled circle of 14px diameter in dark gray (#3a3a3a) is displayed at the marker's coordinate, with a 3px white glow ring separating it from the route line

#### Scenario: Marker text label
- **WHEN** a distance marker is rendered
- **THEN** a text label with format "{N} km" is displayed offset from the dot, using 12px font size in earth-tone dark color (#2c2416) on a semi-transparent white background
