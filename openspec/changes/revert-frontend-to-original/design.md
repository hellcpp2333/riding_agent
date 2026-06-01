## Context

The frontend redesign change (`redesign-frontend-with-web-design-guidelines`) replaced the original `static/index.html` with a rewritten version and added `static/css/style.css`. The user wants to revert to the original single-file frontend.

## Goals / Non-Goals

**Goals:**
- Delete `static/css/style.css`
- Restore `static/index.html` to its pre-redesign state (commit `4430ab2` or equivalent)
- Restore all original inline styles, no theme toggle, no dark mode

**Non-Goals:**
- No backend changes
- No data migration
- No other files touched

## Decisions

**Approach:** Use `git checkout <commit> -- static/index.html` to restore the original file, then delete `static/css/style.css`.
**Rationale:** Simplest, most reliable approach. Guarantees bit-exact restoration.
**Alternative considered:** Manually rewriting the original HTML — rejected because git checkout is faster and guarantees exact match.

## Risks / Trade-offs

None — this is a straightforward revert with no risk.
