## Why

The current frontend (`static/index.html`) violates numerous Vercel Web Interface Guidelines — missing focus indicators, `transition: all` anti-pattern, no `prefers-reduced-motion`, icon-only buttons without `aria-label`, hardcoded date formats, `outline: none` without replacement, form inputs lacking `autocomplete`, and missing `touch-action: manipulation`. A guidelines-compliant refresh will improve both aesthetics and accessibility while preserving the proven sidebar+map layout.

## What Changes

- Replace inline `<style>` with extracted `static/css/style.css` using CSS custom properties (light theme only)
- Fix anti-patterns: `transition: all` → explicit properties, `outline: none` → `:focus-visible` ring, add `prefers-reduced-motion` support
- Add visible focus indicators on all interactive elements (inputs, buttons, nav tabs)
- Polish auth pages: branded gradient + logo, refined form cards with proper labels and autocomplete
- Improve chat UI: refined message bubbles, tool-call pulse indicator, input focus glow
- Enhance route management: card hover/selection with focus-visible, empty state illustration
- Add map route info overlay for selected routes
- Apply consistent transitions (opacity + transform only), add message fade-in animation
- Fix typography: ellipsis `…`, non-breaking spaces for units
- Add `touch-action: manipulation` for mobile, `overscroll-behavior: contain` in modals
- Button hover states throughout, Element Plus theme overrides
- **Map layout preserved exactly**: `#sidebar` 380px + `#map-container` flex:1, no responsive hiding

## Capabilities

### New Capabilities
- `ui-accessibility`: Visible focus states, aria-labels, prefers-reduced-motion, proper form labeling, semantic interaction
- `polished-ui`: Design tokens, refined auth/chat/route cards, transitions, map info overlay
- `anti-pattern-fix`: Remove all flagged anti-patterns (transition:all, outline:none, missing labels, hardcoded formats)

### Modified Capabilities
None.

## Impact

- `static/index.html` — `<style>` block replaced with `<link>`, minor HTML additions (brand area, aria-labels, overlay)
- New `static/css/style.css` — extracted design tokens and component styles, guidelines-compliant
- No backend changes, no new CDN dependencies
- Map layout byte-identical to original
