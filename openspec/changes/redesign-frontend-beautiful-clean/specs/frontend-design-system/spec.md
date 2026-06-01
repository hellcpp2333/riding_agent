## ADDED Requirements

### Requirement: Design System Tokens
The frontend SHALL use CSS custom properties (design tokens) defined in `:root` selector for all colors, spacing, typography, shadows, and border radii.

#### Scenario: Color tokens are defined
- **WHEN** the CSS file is loaded
- **THEN** the following color tokens MUST be defined in `:root`:
  - `--color-bg`: Main background color
  - `--color-bg-sidebar`: Sidebar background color
  - `--color-surface`: Card/surface background color
  - `--color-surface-hover`: Hover state for surfaces
  - `--color-surface-secondary`: Secondary surface color
  - `--color-text`: Primary text color
  - `--color-text-secondary`: Secondary text color
  - `--color-text-tertiary`: Tertiary/placeholder text color
  - `--color-text-inverse`: Inverse text color (on dark backgrounds)
  - `--color-primary`: Primary action color
  - `--color-primary-hover`: Hover state for primary color
  - `--color-primary-active`: Active state for primary color
  - `--color-primary-muted`: Muted version of primary color
  - `--color-primary-glow`: Glow effect for focus states
  - `--color-success`: Success state color
  - `--color-success-muted`: Muted success color
  - `--color-warning`: Warning state color
  - `--color-warning-muted`: Muted warning color
  - `--color-error`: Error state color
  - `--color-error-muted`: Muted error color
  - `--color-info`: Info state color
  - `--color-info-muted`: Muted info color
  - `--color-border`: Border color
  - `--color-border-light`: Light border color
  - `--color-border-focus`: Focus border color

#### Scenario: Spacing tokens are defined
- **WHEN** the CSS file is loaded
- **THEN** the following spacing tokens MUST be defined in `:root`:
  - `--space-1`: 4px
  - `--space-2`: 8px
  - `--space-3`: 12px
  - `--space-4`: 16px
  - `--space-5`: 20px
  - `--space-6`: 24px
  - `--space-8`: 32px
  - `--space-10`: 40px

#### Scenario: Typography tokens are defined
- **WHEN** the CSS file is loaded
- **THEN** the following typography tokens MUST be defined in `:root`:
  - `--font-xs`: 12px
  - `--font-sm`: 13px
  - `--font-md`: 14px
  - `--font-lg`: 16px
  - `--font-xl`: 18px
  - `--font-2xl`: 22px
  - `--font-weight-normal`: 400
  - `--font-weight-medium`: 500
  - `--font-weight-semibold`: 600
  - `--font-weight-bold`: 700
  - `--letter-spacing-heading`: 0.02em

#### Scenario: Radius tokens are defined
- **WHEN** the CSS file is loaded
- **THEN** the following radius tokens MUST be defined in `:root`:
  - `--radius-sm`: 4px
  - `--radius-md`: 8px
  - `--radius-lg`: 12px
  - `--radius-xl`: 16px
  - `--radius-full`: 9999px

#### Scenario: Shadow tokens are defined
- **WHEN** the CSS file is loaded
- **THEN** the following shadow tokens MUST be defined in `:root`:
  - `--shadow-sm`: Small shadow for subtle elevation
  - `--shadow-md`: Medium shadow for cards
  - `--shadow-lg`: Large shadow for modals/dropdowns
  - `--shadow-glow`: Glow effect for focus states

#### Scenario: Transition tokens are defined
- **WHEN** the CSS file is loaded
- **THEN** the following transition tokens MUST be defined in `:root`:
  - `--transition-fast`: 150ms ease
  - `--transition-base`: 200ms ease

### Requirement: Standalone Stylesheet
The frontend SHALL extract all CSS from the inline `<style>` block into a standalone file at `static/css/style.css`.

#### Scenario: Stylesheet is linked in HTML
- **WHEN** the index.html is loaded
- **THEN** the HTML MUST include `<link rel="stylesheet" href="/static/css/style.css">`

#### Scenario: Inline styles are removed
- **WHEN** the redesign is complete
- **THEN** the HTML MUST NOT contain any inline `<style>` blocks

### Requirement: Auth Pages Styling
The login and register pages SHALL use the design system tokens with a cohesive visual appearance.

#### Scenario: Auth container background
- **WHEN** viewing the login/register page
- **THEN** the auth container MUST have a gradient background defined by `--gradient-auth`

#### Scenario: Auth card styling
- **WHEN** viewing the auth card
- **THEN** the card MUST use `--color-surface` background with `--radius-xl` border radius

#### Scenario: Auth switch link
- **WHEN** viewing the auth switch text
- **THEN** the link color MUST be `--color-primary` with hover transition

### Requirement: Main App Layout Styling
The main application layout SHALL use design system tokens for consistent appearance.

#### Scenario: Sidebar styling
- **WHEN** viewing the sidebar
- **THEN** the sidebar MUST use `--color-bg-sidebar` background with `--color-border` right border

#### Scenario: Header styling
- **WHEN** viewing the header
- **THEN** the header MUST use `--color-surface` background with `--color-border` bottom border

#### Scenario: Navigation tabs
- **WHEN** viewing navigation tabs
- **THEN** the active tab MUST use `--color-primary` background with white text

### Requirement: Chat Interface Styling
The chat messages and input area SHALL use design system tokens with improved visual hierarchy.

#### Scenario: User message bubble
- **WHEN** viewing a user message
- **THEN** the bubble MUST use `--color-primary` background with white text and `--radius-lg` border radius

#### Scenario: Assistant message bubble
- **WHEN** viewing an assistant message
- **THEN** the bubble MUST use `--color-surface` background with `--color-text` text and `--radius-lg` border radius

#### Scenario: Input field focus state
- **WHEN** the message input is focused
- **THEN** the border color MUST be `--color-border-focus` with `--shadow-glow` effect

### Requirement: Map API Key Configuration
The Baidu Maps JS API key MUST be properly configured for map rendering.

#### Scenario: Placeholder is maintained in HTML
- **WHEN** viewing index.html
- **THEN** the script tag MUST use `__BAIDU_MAPS_JS_AK__` as the AK parameter

#### Scenario: API key is set in environment
- **WHEN** the application starts
- **THEN** the `BAIDU_MAPS_JS_AK` environment variable MUST be set to a valid Baidu Maps API key

#### Scenario: API key is replaced at runtime
- **WHEN** the root endpoint is requested
- **THEN** main.py MUST replace `__BAIDU_MAPS_JS_AK__` with the value from `os.environ["BAIDU_MAPS_JS_AK"]`