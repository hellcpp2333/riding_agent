## ADDED Requirements

### Requirement: No transition all
No CSS rule SHALL use `transition: all`. All transitions SHALL list specific properties (e.g., `transition: border-color 200ms ease, box-shadow 200ms ease`).

#### Scenario: Explicit transitions
- **WHEN** any CSS transition is defined
- **THEN** the properties SHALL be listed explicitly, never `all`

### Requirement: No bare outline none
No element SHALL use `outline: none` or `outline:none` without providing a visible `:focus-visible` replacement.

#### Scenario: Focus replacement
- **WHEN** outline is removed from an interactive element
- **THEN** a visible `:focus-visible` style (ring, glow, border change) SHALL be present

### Requirement: Proper ellipsis
Loading states, placeholders, and truncated text SHALL use the ellipsis character `…` (U+2026) instead of three dots `...`.

#### Scenario: Loading text
- **WHEN** a loading indicator text is displayed
- **THEN** it SHALL use `…` not `...`

### Requirement: Non-breaking space for units
Numeric values with units SHALL use `&nbsp;` between the number and unit (e.g., `10&nbsp;km`).

#### Scenario: Distance display
- **WHEN** distance is displayed in route cards
- **THEN** the value and unit SHALL be separated by a non-breaking space
