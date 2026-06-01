## ADDED Requirements

### Requirement: Branded auth layout
The auth pages SHALL feature a branded gradient background with the app logo/name prominently displayed above the login/register card.

#### Scenario: Auth page hero section
- **WHEN** user visits the auth page (not logged in)
- **THEN** the background shows a subtle cycling-themed gradient, with "骑行路线助手" text and a bike icon visible above the form card

### Requirement: Auth form card refinement
The login and register forms SHALL use consistent spacing, clear labels, and smooth error/success feedback animations.

#### Scenario: Form field spacing
- **WHEN** the auth form is displayed
- **THEN** form fields have 16px vertical spacing, labels are 13px with 4px bottom margin, and input heights are 44px

#### Scenario: Form validation feedback
- **WHEN** a form validation error occurs
- **THEN** the error message appears with a fade-in animation and the input border changes to --color-error

#### Scenario: Loading state on submit
- **WHEN** user submits the auth form
- **THEN** the submit button shows a spinner and is disabled until the request completes

### Requirement: Toggle between login and register
The system SHALL provide a smooth transition when switching between login and register modes within the same card.

#### Scenario: Mode switch animation
- **WHEN** user clicks "立即注册" or "去登录"
- **THEN** the form content slides/fades to the other form within 300ms without page reload
