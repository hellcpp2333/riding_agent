## ADDED Requirements

### Requirement: Route card design
Route cards in the management view SHALL use a card-based layout with consistent styling, hover effects, and a clear selected state.

#### Scenario: Route card hover
- **WHEN** user hovers over a route card
- **THEN** the card SHALL show a border color change and subtle shadow lift

#### Scenario: Route card selected
- **WHEN** a route is selected
- **THEN** the card SHALL show a distinct background tint and persistent border color

#### Scenario: Route card metadata
- **WHEN** a route card is displayed
- **THEN** it SHALL show the route name, source badge, distance, and date in a clear hierarchy

### Requirement: Empty state
The route management view SHALL display an illustrated empty state when no routes exist.

#### Scenario: No routes saved
- **WHEN** the user has zero saved routes
- **THEN** a centered illustration with icon and guidance text SHALL be shown

### Requirement: Map route info overlay
When a route is selected, a floating info card SHALL appear on the map showing route name, distance, and elevation.

#### Scenario: Route info card
- **WHEN** a route track is rendered on the map
- **THEN** a small info card SHALL be displayed at the bottom of the map panel with key route stats
