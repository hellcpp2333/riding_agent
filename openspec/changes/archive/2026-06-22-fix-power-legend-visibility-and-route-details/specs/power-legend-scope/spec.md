## ADDED Requirements

### Requirement: Power legend visible only on activities tab with selected activity

The system SHALL display the power zone legend overlay on the map ONLY when all of the following conditions are met:
- The user is on the "运动" (activities) tab
- A specific activity record is selected (not the activity list view)
- The selected activity has power segment data available

The power zone legend SHALL NOT be displayed on the map when the user is on the "对话" (chat) tab or the "路书" (routes) tab, regardless of any prior activity selection.

#### Scenario: User views activity with power data

- **WHEN** user is on the activities tab AND selects an activity that has power data
- **THEN** the power zone legend is displayed on the map

#### Scenario: User views activity without power data

- **WHEN** user is on the activities tab AND selects an activity that has no power data
- **THEN** the power zone legend is NOT displayed on the map

#### Scenario: User switches to chat tab after viewing activity

- **WHEN** user was viewing an activity with power data AND switches to the chat tab
- **THEN** the power zone legend is hidden from the map

#### Scenario: User switches to routes tab after viewing activity

- **WHEN** user was viewing an activity with power data AND switches to the routes tab
- **THEN** the power zone legend is hidden from the map

#### Scenario: User on activity list view

- **WHEN** user is on the activities tab but no specific activity is selected (viewing activity list)
- **THEN** the power zone legend is NOT displayed on the map

### Requirement: Route details display correctly after tab switch

The system SHALL correctly load and display all route details (including climb segments, elevation panel, and distance markers) when the user selects a route on the routes tab, regardless of prior interactions on the activities tab or chat tab.

#### Scenario: Select route after viewing activity with power data

- **WHEN** user viewed an activity with power data on the activities tab AND then switches to the routes tab AND selects a route that has elevation data with climb segments
- **THEN** the route's climb segments are highlighted on the map AND the elevation panel shows distance/gain/loss stats AND the power zone legend is NOT displayed

#### Scenario: Select route after viewing activity without power data

- **WHEN** user viewed an activity without power data on the activities tab AND then switches to the routes tab AND selects a route with elevation data
- **THEN** the route is displayed with all its details (climb segments, elevation panel) AND no residual activity state is visible

#### Scenario: Switch between multiple routes

- **WHEN** user selects route A (with climb segments) AND then selects route B (without climb segments)
- **THEN** route A's climb segments are removed from the map AND route B's details (possibly without climb segments) are displayed correctly
