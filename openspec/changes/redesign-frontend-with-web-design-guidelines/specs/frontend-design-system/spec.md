## ADDED Requirements

### Requirement: CSS design tokens
The system SHALL define CSS custom properties for colors, spacing, typography, border radii, and shadows in a standalone `static/css/style.css` file that all UI elements reference.

#### Scenario: All visual values come from tokens
- **WHEN** any UI element is styled
- **THEN** color, spacing, font-size, border-radius, and shadow values MUST be CSS custom property references (e.g., `var(--color-primary)`) rather than hardcoded values

#### Scenario: Dark and light themes defined
- **WHEN** the page loads
- **THEN** the `[data-theme="dark"]` selector provides a full set of token values suitable for dark backgrounds, and `[data-theme="light"]` provides values for light backgrounds

### Requirement: Consistent typography scale
The system SHALL use a defined typography scale with 5 levels (xs, sm, md, lg, xl) mapped to CSS custom properties.

#### Scenario: Typography tokens used throughout
- **WHEN** text content is rendered
- **THEN** font sizes reference `--font-size-*` tokens, line heights reference `--line-height-*` tokens, and font weights reference `--font-weight-*` tokens

### Requirement: Consistent spacing scale
The system SHALL use a spacing scale (4px base unit with multipliers: 1, 2, 3, 4, 6, 8, 12, 16) mapped to CSS custom properties.

#### Scenario: Spacing uses tokens
- **WHEN** padding, margin, or gap is set
- **THEN** the value references `--space-*` tokens rather than arbitrary pixel values

### Requirement: Consistent interactive states
All interactive elements (buttons, links, inputs, cards) SHALL have defined hover, focus, active, and disabled states with smooth CSS transitions.

#### Scenario: Button hover transition
- **WHEN** user hovers over a button
- **THEN** the button smoothly transitions to its hover style within 200ms

#### Scenario: Focus ring on inputs
- **WHEN** an input receives keyboard focus
- **THEN** a visible focus ring appears using `--color-focus-ring`
