## ADDED Requirements

### Requirement: Responsive sidebar
The system SHALL adapt the sidebar layout based on viewport width. At widths >= 768px, the sidebar SHALL display alongside the map panel. At widths < 768px, the sidebar SHALL occupy full width and height, with the map accessible via a toggle.

#### Scenario: Desktop layout shows sidebar and map side by side
- **WHEN** viewport width is >= 768px
- **THEN** the sidebar (380px) is fixed on the left and the map fills the remaining width

#### Scenario: Mobile layout shows full-width sidebar
- **WHEN** viewport width is < 768px
- **THEN** the sidebar occupies 100% width, and a floating "Show Map" button is visible

#### Scenario: Map toggle on mobile
- **WHEN** user taps "Show Map" on mobile
- **THEN** the map panel slides in to cover the viewport, with a "Back" button to return to the sidebar

### Requirement: Responsive auth pages
The auth page cards SHALL remain usable on small screens without horizontal scrolling.

#### Scenario: Auth card on mobile
- **WHEN** viewport width is < 480px
- **THEN** the auth card width is `min(90vw, 400px)` and padding reduces to 24px

### Requirement: Responsive modals
Modal dialogs SHALL be usable on mobile without overflowing the viewport.

#### Scenario: Modal on mobile
- **WHEN** viewport width is < 768px and a modal is open
- **THEN** the modal content width is `min(95vw, 500px)` and content scrolls internally if taller than 80vh

### Requirement: Touch-friendly tap targets
Interactive elements on mobile SHALL meet minimum touch target size of 44x44px.

#### Scenario: Buttons and links on mobile
- **WHEN** viewport width is < 768px
- **THEN** all buttons, nav tabs, and clickable icons have min-height and min-width of at least 44px
