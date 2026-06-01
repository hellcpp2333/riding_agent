## Why

Reverting the latest frontend UI polish change (`polish-ui-preserve-map-layout`), restoring the original single-file frontend with inline CSS.

## What Changes

- Delete `static/css/style.css`
- Restore `static/index.html` to its original state (inline `<style>` block, no external CSS, no design tokens)

## Capabilities

### New Capabilities
None — pure revert.

### Modified Capabilities
None.

## Impact

- `static/css/style.css` — deleted
- `static/index.html` — restored via `git restore`
