## ADDED Requirements

### Requirement: Header and navigation styling
The sidebar header SHALL use consistent spacing, defined color tokens, and clear active-state indicators for navigation tabs.

#### Scenario: Nav tab active state
- **WHEN** a navigation tab ("对话" or "路书") is active
- **THEN** the tab SHALL have a prominent background color and the inactive tabs SHALL show hover feedback

#### Scenario: Session selector styling
- **WHEN** the session selector is displayed
- **THEN** it SHALL have a consistent border, padding, and focus ring using design tokens

#### Scenario: New session button
- **WHEN** the new session button is displayed
- **THEN** it SHALL use a distinct accent color with hover transition

### Requirement: User menu consistency
The user avatar and dropdown menu SHALL use design token colors for borders and backgrounds.

#### Scenario: Avatar hover
- **WHEN** user hovers over the avatar
- **THEN** the border color SHALL transition smoothly to the primary color
