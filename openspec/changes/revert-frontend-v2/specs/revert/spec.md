## ADDED Requirements

### Requirement: Original frontend restored
The system SHALL use the original single-file frontend with inline CSS only.

#### Scenario: No external stylesheet
- **WHEN** the application loads
- **THEN** no `static/css/style.css` exists and all styles are inline
