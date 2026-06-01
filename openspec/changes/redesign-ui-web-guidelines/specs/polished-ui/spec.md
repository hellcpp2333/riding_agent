## ADDED Requirements

### Requirement: Design tokens
The system SHALL use CSS custom properties for all visual values (colors, spacing, typography, radii, shadows) in an external `static/css/style.css`.

#### Scenario: Token-based styling
- **WHEN** any element is styled
- **THEN** color, spacing, and radius values SHALL reference CSS custom properties

### Requirement: Branded auth pages
Auth pages SHALL have a cycling-themed gradient background with app branding (icon, title, subtitle) above the form card. Form inputs SHALL be 44px tall with proper labels and autocomplete.

#### Scenario: Auth page branding
- **WHEN** user is not authenticated
- **THEN** branding (icon + title + subtitle) SHALL be visible above the login/register card

### Requirement: Refined chat messages
Message bubbles SHALL use distinct styles for user and assistant, with fade-in animations.

#### Scenario: Message bubble distinction
- **WHEN** messages are displayed
- **THEN** user messages SHALL be right-aligned with colored background, assistant messages left-aligned with light background and border

### Requirement: Route card polish
Route cards SHALL have hover elevation, selected state highlight, and empty state illustration.

#### Scenario: Card hover and selection
- **WHEN** user hovers a route card
- **THEN** border color SHALL change and a subtle shadow SHALL appear
- **WHEN** user selects a route card
- **THEN** the card SHALL show a distinct background tint

### Requirement: Map route info overlay
When a route is selected and rendered on the map, a floating info card SHALL display route name, distance, and elevation.

#### Scenario: Route info display
- **WHEN** a route track is on the map
- **THEN** an info card SHALL appear at the bottom of the map panel
