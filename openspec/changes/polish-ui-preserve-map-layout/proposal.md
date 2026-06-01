## Why

The frontend is functional but visually dated — raw inline CSS with no design system, no transitions, and dated spacing/typography. However, the sidebar+map split layout works well for the cycling use case and must be preserved. A targeted polish of the sidebar UI (auth, chat, routes, header) will improve the visual quality without disrupting the proven map layout.

## What Changes

- Replace inline `<style>` block with a linked `static/css/style.css` using CSS custom properties (design tokens)
- Modernize the auth pages with a cycling-themed gradient, app branding, and refined form cards
- Polish the sidebar header with consistent spacing, improved nav-tab active states, session selector, and new-session button
- Refine chat message bubbles (color, spacing, border-radius) and add message fade-in animation
- Add tool-call status indicator with pulse animation
- Improve route management cards with hover effects, selection state, and empty-state illustration
- Enhance input area with focus glow and send-button loading states
- Add smooth hover/focus/active transitions on all interactive elements
- **地图布局保持在 sidebar 右侧，Flexbox 布局不受影响**

## Capabilities

### New Capabilities
- `sidebar-ui-polish`: Refined sidebar styling — header, nav tabs, session controls, user menu, with consistent tokens and transitions
- `polished-auth`: Branded login/register pages with gradient background, logo, and refined form cards
- `modern-chat`: Polished message bubbles, tool indicators, and input area with transitions
- `route-card-polish`: Refined route management cards with hover, selection, and empty states

### Modified Capabilities
None — no requirement-level changes. All existing functionality preserved.

## Impact

- `static/index.html` — `<style>` block rewritten to reference `static/css/style.css`; HTML structure keeps the same sidebar+map layout
- New `static/css/style.css` — extracted design tokens and component styles
- No map layout changes (`#map-container`, `#map`, `.main-app { display: flex }` all preserved)
- No responsive breakpoints that affect map visibility
- No dark/light theme toggle
- No backend or API changes
