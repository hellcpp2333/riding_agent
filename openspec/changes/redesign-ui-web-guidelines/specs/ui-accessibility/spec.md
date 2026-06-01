## ADDED Requirements

### Requirement: Visible focus states
All interactive elements SHALL have visible focus indicators using `:focus-visible` with a box-shadow ring. No element SHALL use `outline: none` without a replacement focus style.

#### Scenario: Input focus ring
- **WHEN** an input receives keyboard focus via Tab
- **THEN** a visible ring SHALL appear around the input

#### Scenario: Button focus ring
- **WHEN** a button receives keyboard focus
- **THEN** a visible ring SHALL appear

### Requirement: Reduced motion support
All animations and transitions SHALL be disabled or reduced when the user has `prefers-reduced-motion: reduce` set.

#### Scenario: Reduced motion active
- **WHEN** user has `prefers-reduced-motion: reduce`
- **THEN** animations SHALL be instant (0s duration) and transitions SHALL be disabled

### Requirement: Icon-only button labels
Icon-only buttons (export, delete) SHALL have `aria-label` attributes.

#### Scenario: Icon button accessibility
- **WHEN** an icon-only button is rendered
- **THEN** it SHALL have a descriptive `aria-label`

### Requirement: Touch interaction
Interactive elements SHALL use `touch-action: manipulation` to prevent double-tap zoom delay. Modals SHALL use `overscroll-behavior: contain`.

#### Scenario: Touch optimization
- **WHEN** user interacts on a touch device
- **THEN** double-tap zoom SHALL not be triggered on buttons and inputs
