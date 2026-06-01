## ADDED Requirements

### Requirement: Original frontend restored
The system SHALL use the original single-file frontend (`static/index.html`) with all inline CSS and no separate design system stylesheet.

#### Scenario: No external stylesheet
- **WHEN** the application is loaded
- **THEN** no `static/css/style.css` file is present and all styles are inline in `static/index.html`

#### Scenario: Original layout restored
- **WHEN** the main app is displayed
- **THEN** the layout matches the pre-redesign version with original colors, spacing, and no theme toggle
