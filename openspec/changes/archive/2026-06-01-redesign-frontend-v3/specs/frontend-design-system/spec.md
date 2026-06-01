## ADDED Requirements

### Requirement: Design System Tokens
CSS custom properties SHALL be defined in `:root` for colors, spacing, typography, radii, shadows, and transitions.

#### Scenario: Tokens are defined
- **WHEN** `static/css/style.css` is loaded
- **THEN** color tokens (--color-bg, --color-primary, --color-text, etc.) MUST be present
- **AND** spacing tokens (--space-1 to --space-10) MUST be present
- **AND** typography tokens (--font-xs to --font-2xl) MUST be present
- **AND** radius and shadow tokens MUST be present

### Requirement: Standalone Stylesheet
CSS MUST be in `static/css/style.css`, not inline in HTML.

#### Scenario: No inline styles
- **WHEN** redesign is complete
- **THEN** `static/index.html` MUST NOT contain `<style>` tags
- **AND** MUST include `<link rel="stylesheet" href="/static/css/style.css">`

### Requirement: Static File Serving
The application SHALL serve files from the `static/` directory.

#### Scenario: CSS is accessible
- **WHEN** requesting `/static/css/style.css`
- **THEN** the server MUST return HTTP 200 with the CSS content

### Requirement: Auth Pages Styling
Login and register pages SHALL use design tokens with gradient background.

#### Scenario: Auth container
- **WHEN** viewing auth page
- **THEN** container MUST use `--gradient-auth` background
- **AND** card MUST use `--color-surface` with `--radius-xl`

### Requirement: Chat Interface Styling
Messages SHALL use distinct bubble styles with fade-in animation.

#### Scenario: Message bubbles
- **WHEN** viewing chat messages
- **THEN** user messages MUST use `--color-primary` background
- **AND** assistant messages MUST use `--color-surface` background with border

### Requirement: Map API Key Configuration
Baidu Maps JS API key MUST be properly configured for map rendering.

#### Scenario: Map script loads with correct key
- **WHEN** accessing the root page
- **THEN** the HTML MUST contain a Baidu Maps script tag with a valid AK value