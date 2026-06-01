## ADDED Requirements

### Requirement: Polished message bubbles
Chat messages SHALL use refined, distinctive bubble styles with subtle fade-in animation.

#### Scenario: Message display
- **WHEN** messages are rendered
- **THEN** user messages SHALL be right-aligned with primary background, assistant messages left-aligned with elevated card style

### Requirement: Route card polish
Route cards SHALL have hover elevation, selected state, and icon-based source indicators.

#### Scenario: Card interaction
- **WHEN** user hovers a route card
- **THEN** the card SHALL lift with a shadow and border color change
- **WHEN** user selects a route card  
- **THEN** the card SHALL show a tinted background

### Requirement: Map route overlay
When a route is selected and displayed on the map, SHALL show a floating info card with route stats.

#### Scenario: Route info display
- **WHEN** a route track is on the map
- **THEN** an info card SHALL appear at bottom of map panel

### Requirement: Map loads correctly
BMapGL initialization and the `#map-container` / `#map` CSS SHALL be identical to the original.

#### Scenario: Map unchanged
- **WHEN** the app loads after authentication
- **THEN** the map SHALL initialize and display exactly as it did before the redesign
