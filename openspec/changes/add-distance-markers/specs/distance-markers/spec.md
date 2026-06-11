## ADDED Requirements

### Requirement: Route distance markers
The system SHALL display distance markers at 5km intervals along any route polyline rendered on the map, including both chat-planned routes and imported route books.

#### Scenario: Markers appear on chat-planned route
- **WHEN** a route with total distance ≥ 5km is drawn on the map via chat planning
- **THEN** distance markers appear at 5km, 10km, 15km, ... up to the last full 5km mark before the route end
- **THEN** each marker displays a circular dot on the route line and a text label showing the distance (e.g., "5 km")

#### Scenario: Markers appear on imported route
- **WHEN** a saved route book is selected and rendered on the map with distance ≥ 5km
- **THEN** distance markers appear at 5km intervals along the imported track

#### Scenario: Short routes get no markers
- **WHEN** a route with total distance < 5km is drawn on the map
- **THEN** no distance markers are displayed

#### Scenario: Marker positions are accurate
- **WHEN** distance markers are generated along a route
- **THEN** each marker is positioned within 50m of the true 5km-interval distance along the route path, using Haversine cumulative distance and linear interpolation between adjacent path points

### Requirement: Distance marker visual style
Distance markers SHALL use a Garmin-style visual design with a filled circular dot and distance text label.

#### Scenario: Marker dot appearance
- **WHEN** a distance marker is rendered
- **THEN** a filled circle of 8px diameter in dark gray (#3a3a3a) is displayed at the marker's coordinate

#### Scenario: Marker text label
- **WHEN** a distance marker is rendered
- **THEN** a text label with format "{N} km" is displayed offset from the dot, using earth-tone dark color (#2c2416) on a semi-transparent white background

### Requirement: Marker lifecycle
Distance markers SHALL be removed when the corresponding route is cleared from the map.

#### Scenario: Markers cleared with route
- **WHEN** `clearMap()` or `clearMapOverlays()` is called
- **THEN** all distance markers are removed from the map and their references are cleared
