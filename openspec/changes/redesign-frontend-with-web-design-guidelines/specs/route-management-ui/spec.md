## ADDED Requirements

### Requirement: Route card design
Route cards in the management view SHALL use a card-based layout with route name, metadata, source badge, and action buttons.

#### Scenario: Route card layout
- **WHEN** the route management tab is active
- **THEN** each route is displayed as a card with icon, route name (bold), distance, elevation gain, date, source badge ("导入" or "Agent"), and action buttons (export, delete)

#### Scenario: Route card hover and selection
- **WHEN** user hovers over a route card
- **THEN** the card border color transitions to `--color-primary` with a subtle shadow lift
- **WHEN** a route is selected
- **THEN** the card background changes to a tinted variant and border remains `--color-primary`

#### Scenario: Route distance visualization
- **WHEN** a route card is displayed
- **THEN** the distance is formatted as "XX.X km" and a small bar indicator shows relative length compared to other routes

### Requirement: Empty state
The route management view SHALL display an illustrative empty state when no routes exist.

#### Scenario: No routes saved
- **WHEN** the user has no saved routes
- **THEN** a centered empty state is shown with a cycling icon, "还没有路书" message, and a prompt to "导入 GPX 文件开始"

### Requirement: Import button and feedback
The import button SHALL provide clear visual feedback during and after file upload.

#### Scenario: Import button styling
- **WHEN** the route management tab is active
- **THEN** a prominent import button is shown in the toolbar with `--color-primary` background and a "+" icon

#### Scenario: Import success feedback
- **WHEN** a GPX file is successfully imported
- **THEN** a success toast appears with the route name and distance, and the route list updates with a fade-in animation for the new entry

### Requirement: Route detail on map
Selecting a route SHALL render the track on the map with start/end markers and a summary overlay.

#### Scenario: Route track rendering
- **WHEN** user clicks a route card
- **THEN** the map draws the route track with `--color-success` stroke color, start (green) and end (red) markers, and the viewport fits the route bounds

#### Scenario: Route summary overlay
- **WHEN** a route is selected on the map
- **THEN** a floating info card appears at the bottom of the map showing route name, distance, and elevation gain
