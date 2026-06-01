## Why

The frontend redesign introduced visual and functional changes that diverged from the original working state. The user wants the pre-redesign frontend restored — the version at commit `4430ab2` (HEAD~1 before the redesign) with all inline styles and no separate CSS file.

## What Changes

- Remove `static/css/style.css` — the extracted design system file
- Restore `static/index.html` to its original state (single-file, inline CSS, no theme toggle, no dark mode, no responsive layout, no new animations)
- Remove the theme toggle button and dark/light theme logic from JS

## Capabilities

### New Capabilities
None — this is a pure revert with no new capabilities.

### Modified Capabilities
None — no requirement changes.

## Impact

- `static/css/style.css` — deleted
- `static/index.html` — restored to original (pre-redesign) version
- No backend or API changes
