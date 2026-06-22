## ADDED Requirements

### Requirement: Route elevation panel and climb segments load despite overlay cleanup errors

The system SHALL display the route elevation panel (distance, elevation gain, elevation loss) and climb segments on the map when a route is selected on the routes tab, even if the preceding map overlay cleanup encounters errors.

#### Scenario: Select route after viewing activity with power data

- **WHEN** user viewed an activity with power-colored route segments on the activities tab AND switches to routes tab AND selects a route that has elevation data with climb segments
- **THEN** the elevation panel shows distance/gain/loss stats AND climb segments are highlighted on the map AND the route track is displayed

#### Scenario: Select route with overlay cleanup failure

- **WHEN** user selects a route AND `map.removeOverlay()` throws an error during overlay cleanup
- **THEN** the error is caught and ignored AND the route track, elevation panel, and climb segments are still loaded and displayed

#### Scenario: Select route without elevation data

- **WHEN** user selects a route whose backend elevation enrichment returned null
- **THEN** the route track is displayed on the map AND the elevation panel remains hidden AND no error message is shown to the user

#### Scenario: Elevation gain is missing from API response

- **WHEN** user selects a route AND the API response has `elevation_gain` as undefined
- **THEN** the success message shows "爬升0m" instead of throwing a TypeError AND the route is displayed correctly
