## ADDED Requirements

### Requirement: Power-colored route rendering on map
The frontend SHALL render an uploaded activity's route on the map using different colors for segments of different power zones, following the Garmin Connect 7-zone color scheme.

| Zone | Hex Color |
|------|-----------|
| Z1 | `#A0A0A0` |
| Z2 | `#3498DB` |
| Z3 | `#2ECC71` |
| Z4 | `#F1C40F` |
| Z5 | `#E67E22` |
| Z6 | `#E74C3C` |
| Z7 | `#8E44AD` |
| Z0 | `#D3D3D3` |

#### Scenario: Activity has power segments data
- **WHEN** the activity detail API response includes a non-empty `power_segments` array
- **THEN** the map SHALL render each segment as a separate `BMapGL.Polyline` with the stroke color corresponding to its power zone
- **AND** each polyline SHALL use `strokeWeight: 5` and `strokeOpacity: 0.8`

#### Scenario: Activity has no power data
- **WHEN** the activity detail API response has an empty or null `power_segments`
- **THEN** the map SHALL fall back to rendering a single polyline with the default activity route color (`#e53935`)

#### Scenario: FIT upload result has power segments
- **WHEN** a user uploads a FIT file and the result includes `power_segments` in the response
- **THEN** the map SHALL render the route with power-colored segments instead of the default single-color polyline

### Requirement: Power zone legend display
The frontend SHALL display a power zone color legend overlay on the map when power-colored route segments are active.

#### Scenario: Power-colored route is displayed
- **WHEN** the map renders power-colored route segments
- **THEN** a legend overlay SHALL appear at the bottom-left corner of the map
- **AND** the legend SHALL show 7 rows (Z1-Z7), each with a colored dot and the zone name label (Active Recovery / Endurance / Tempo / Threshold / VO2Max / Anaerobic / Neuromuscular)

#### Scenario: Map view switches away from power-colored route
- **WHEN** the user switches to a non-FIT route or clears the map
- **THEN** the power zone legend SHALL be removed from the map

#### Scenario: Legend toggle for space-constrained viewports
- **WHEN** the viewport width is less than 600px (mobile)
- **THEN** the legend SHALL collapse to show only colored dots without labels
- **OR** the legend SHALL be hidden by default with a toggle button to show/hide it

### Requirement: Single color definition source
The power zone color mapping SHALL be defined in exactly one JavaScript constant to ensure consistency between route rendering and legend display.

#### Scenario: Color consistency check
- **WHEN** a segment is classified as Zone 3 (Tempo)
- **THEN** the polyline stroke color and the legend dot color for Zone 3 SHALL reference the same JavaScript constant value
- **AND** the constant SHALL be named `POWER_ZONE_COLORS` and be an array or object indexed by zone number
