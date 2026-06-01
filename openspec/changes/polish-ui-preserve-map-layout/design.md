## Context

The current frontend is a single `static/index.html` with an inline `<style>` block and inline `<script>` using Vue 3 + Element Plus via CDN. The sidebar+map flexbox layout is proven and works well for the cycling use case. The UI is functional but lacks visual polish — raw color values, no design tokens, no transitions, dated spacing.

## Goals / Non-Goals

**Goals:**
- Extract CSS into `static/css/style.css` with CSS custom properties (design tokens) for colors, spacing, typography, radii, shadows
- Light theme only (no dark mode toggle, no theme switching)
- Polish auth pages (branded gradient, logo, refined card)
- Refine sidebar header (nav tabs, session controls, user menu)
- Improve chat messages (bubble polish, tool indicators, route cards)
- Enhance route management cards (hover, selection, empty state)
- Add smooth transitions on all interactive elements
- **Preserve map layout exactly** — sidebar `380px` on left, map `flex: 1` on right

**Non-Goals:**
- No dark/light theme toggle
- No responsive breakpoints that affect the map panel
- No new JS framework, build system, or CDN dependencies
- No backend changes
- No mobile/tablet responsive layout

## Decisions

### 1. Light-theme-only design tokens
**Choice:** CSS custom properties with fixed light theme values, no `[data-theme]` switching.
**Rationale:** User rejected the dark theme approach. Light theme suits the current Element Plus component defaults. CSS custom properties still provide organization and consistency benefits even without runtime switching.
**Alternative considered:** No design tokens (keep inline) — rejected because organized tokens improve maintainability.

### 2. Map layout untouchable
**Choice:** The entire `.main-app`, `#sidebar`, `#map-container`, `#map` block and all related positioning CSS remains byte-for-byte identical to the original.
**Rationale:** User specifically requested no map layout changes. This is the hard constraint of this redesign.
**Alternative considered:** N/A — constraint is absolute.

### 3. Single extracted stylesheet
**Choice:** One `static/css/style.css` file.
**Rationale:** Matches CDN-based architecture, avoids build steps, easy to revert.

### 4. Keep Element Plus CDN with CSS variable overrides
**Choice:** Continue using Element Plus components but override form input, dialog, and button styles where they appear (auth pages, profile dialog).
**Rationale:** Element Plus components are deeply integrated. Full replacement is high effort for low value.

## Risks / Trade-offs

- **No responsive layout** — Users on small screens will still see the sidebar+map split. Acknowledged limitation of this change scope.
- **Single-file CSS may grow unwieldy** — Mitigated by clear organization with comment section headers.
