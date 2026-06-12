## ADDED Requirements

### Requirement: Climb segment highlight on map
The frontend SHALL visually distinguish the currently selected climb segment from other climb segments on the map, and SHALL pan the map to the selected segment.

#### Scenario: User clicks a climb segment in the list
- **WHEN** user clicks a climb segment item in the climb list
- **THEN** the map SHALL redraw climb polylines with the selected segment at full opacity and heavier weight
- **AND** non-selected segments SHALL render at reduced opacity
- **AND** the map SHALL pan to center the selected segment

#### Scenario: User navigates between climb segments via prev/next
- **WHEN** user clicks the previous or next button in the climb sidebar
- **THEN** the map SHALL update the highlighted segment accordingly
- **AND** the map SHALL pan to the newly selected segment

#### Scenario: No climb segment is selected
- **WHEN** the climb sidebar is closed or no segment is active
- **THEN** all climb polylines SHALL render at default uniform opacity

### Requirement: ElMessageBox polyfill for CDN-blocking resilience
The system SHALL provide a polyfill for `ElMessageBox` so that confirmation dialogs function correctly even when the Element Plus CDN is blocked.

#### Scenario: Element Plus CDN loads successfully
- **WHEN** the Element Plus CDN script loads and `ElMessageBox` is defined
- **THEN** the polyfill SHALL NOT overwrite it
- **AND** confirmation dialogs SHALL use native Element Plus MessageBox

#### Scenario: Element Plus CDN is blocked
- **WHEN** `ElMessageBox` is undefined (CDN blocked by Edge Tracking Prevention)
- **THEN** the polyfill SHALL provide `ElMessageBox.confirm()` using `window.confirm()`
- **AND** confirming SHALL resolve the returned Promise
- **AND** canceling SHALL reject with the string `'cancel'`

### Requirement: Route delete uses unified apiFetch
The route deletion function SHALL use the shared `apiFetch` helper to ensure consistent auth handling.

#### Scenario: Auth token expired during delete
- **WHEN** the delete request returns 401
- **THEN** the `apiFetch` helper SHALL clear the token and redirect to login
