## Why

Current frontend uses plain inline CSS with no design system — minimal visual appeal, no consistent spacing or typography, and no polished interactions. A redesign will create a professional, beautiful UI suitable for a consumer-facing cycling tool.

## What Changes

- Extract inline CSS to `static/css/style.css` with design tokens
- Apply earth-tone color palette and consistent typography
- Add smooth transitions, hover effects, and message animations
- Add `StaticFiles` mount in `main.py` for CSS serving
- Ensure Baidu Maps API key replacement works correctly

## Capabilities

### New Capabilities
- `frontend-design-system`: Cohesive CSS design tokens and component styles
- `map-api-config`: Verify Baidu Maps API key is properly configured for map rendering

### Modified Capabilities
None

## Impact

- `static/index.html` — remove inline `<style>`, add CSS link
- `static/css/style.css` — new file with design system
- `main.py` — add `StaticFiles` mount
- No backend or API changes