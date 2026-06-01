## ADDED Requirements

### Requirement: Earth-tone design tokens
The system SHALL use CSS custom properties defining an organic, outdoor-inspired palette: sage green primary, warm stone backgrounds, clay terracotta accents, off-white surfaces.

#### Scenario: Design token usage
- **WHEN** any UI element is styled
- **THEN** colors SHALL reference CSS custom properties, never hardcoded values

### Requirement: Refined typography
Headings SHALL use generous letter-spacing. Stats SHALL use tabular numbers. System font stack with character.

#### Scenario: Typography consistency
- **WHEN** text is rendered
- **THEN** font sizes and weights SHALL use design tokens
