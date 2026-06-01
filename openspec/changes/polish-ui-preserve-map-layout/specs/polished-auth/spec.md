## ADDED Requirements

### Requirement: Branded auth background
The auth pages SHALL feature a cycling-themed gradient background with the app name and icon displayed above the form card.

#### Scenario: Auth page layout
- **WHEN** user is not authenticated
- **THEN** the page SHALL show a gradient background with "🚲 骑行路线助手" branding and a subtitle above the login/register card

### Requirement: Auth form card refinement
Login and register forms SHALL use consistent spacing, proper input heights (44px), and smooth validation feedback.

#### Scenario: Form input styling
- **WHEN** the auth form is rendered
- **THEN** inputs SHALL have 44px height, 16px vertical spacing, and focus states with a glow effect

#### Scenario: Submit button loading
- **WHEN** the form is submitted
- **THEN** the submit button SHALL show a loading spinner and be disabled until the request completes
