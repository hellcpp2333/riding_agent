## Why

Current frontend is basic with inline CSS styles — plain appearance, minimal visual hierarchy, no design consistency, and the Baidu Maps API key is set as a placeholder causing the map to fail loading. A professional redesign using modern design principles will improve user experience, make the app more trustworthy and enjoyable for cyclists, and fix the map rendering issue.

## What Changes

- Extract inline CSS into a standalone stylesheet with CSS custom properties (design tokens)
- Apply a cohesive color palette and typography system with appropriate contrast
- Add smooth transitions, hover effects, and micro-interactions
- Fix Baidu Maps JS API key configuration to ensure map loads correctly
- Improve overall visual hierarchy and spacing throughout the UI
- Keep existing functionality intact — no breaking changes to features

## Capabilities

### New Capabilities
- `frontend-design-system`: Cohesive CSS design system with tokens (colors, spacing, typography, shadows, radii)
- `map-api-key-configuration`: Proper configuration of Baidu Maps JS API key for map rendering

### Modified Capabilities
None — existing frontend capabilities remain functionally unchanged; this is a visual refresh and map fix.

## Impact

- `static/index.html` — refactor to remove inline `<style>` and add CSS file reference; fix Baidu Maps script src
- New `static/css/` directory — extracted stylesheet with design tokens
- `main.py` — no changes (API key replacement logic is preserved)
- `.env.example` — no changes (documented separately)
- No backend changes, no API changes, no new dependencies