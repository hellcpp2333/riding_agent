## Context

The current frontend is a single `static/index.html` (~1350 lines) with inline `<style>` block and inline `<script>` using Vue 3 + Element Plus via CDN. The UI is functional but lacks visual polish: no design tokens, inconsistent spacing, raw color values, no transitions, and no responsive layout. The app is used by cyclists who may view it outdoors on mobile devices, so readability and contrast matter.

## Goals / Non-Goals

**Goals:**
- Extract CSS into `static/css/style.css` with CSS custom properties (design tokens)
- Dark-first color scheme optimized for outdoor readability, with light mode option
- Consistent spacing scale, typography hierarchy, and border radius system
- Smooth transitions and hover effects on interactive elements
- Responsive layout: sidebar collapses on mobile, map stays full-height
- Polished auth pages with better layout and branding
- Modern chat UI with refined message bubbles, status indicators
- Improved route management cards and empty states
- All existing functionality preserved — pure CSS/HTML restyling

**Non-Goals:**
- No new JS framework or build system (stay with Vue 3 CDN + Element Plus CDN)
- No backend changes
- No new npm dependencies or build pipeline
- No i18n or accessibility audit (though basic a11y will be maintained)
- No PWA/offline support

## Decisions

### 1. Dark-first color scheme
**Choice:** Dark theme as default with CSS custom property toggle for light mode.
**Rationale:** Cyclists often use the app outdoors in bright sunlight where dark UIs cause less glare. CSS custom properties make theme switching trivial.
**Alternative considered:** Light-only theme — rejected because dark theme offers better outdoor readability and feels more modern for a cycling app.

### 2. CSS custom properties (design tokens) over CSS-in-JS or preprocessor
**Choice:** CSS custom properties in a standalone `.css` file.
**Rationale:** No build step needed, works with CDN-based setup, allows runtime theme switching. Keeps the stack simple.
**Alternative considered:** SCSS or Tailwind — rejected because they require a build step, adding complexity that doesn't match the project's CDN-based architecture.

### 3. Single extracted stylesheet
**Choice:** One `static/css/style.css` file rather than multiple CSS files.
**Rationale:** With CDN-based architecture, one file minimizes HTTP requests. The file will be organized into clear sections with comments.
**Alternative considered:** Component-level CSS files — rejected due to no module bundler in the stack.

### 4. Keep Element Plus CDN with CSS variable override
**Choice:** Continue using Element Plus components but override their CSS variables for theming.
**Rationale:** Element Plus supports CSS variable theming natively. Replacing the UI library would require rewriting forms, dialogs, dropdowns, and message components — high effort for low value.
**Alternative considered:** Replace with custom components — rejected as too much work for no functional gain.

### 5. Responsive breakpoints
**Choice:** Single breakpoint at 768px (tablet/mobile). Below breakpoint: sidebar becomes full-width overlay, map hides unless a route is active.
**Rationale:** The map panel is the secondary interaction surface; on small screens, prioritizing chat input is more user-friendly.
**Alternative considered:** Multiple breakpoints — rejected as over-engineering for a single-page app.

### 6. Message rendering & Markdown
**Choice:** Continue with `v-html` rendering with existing `formatText()` escaping, enhanced with a lightweight inline markdown-to-HTML converter for bold, italic, code, links.
**Rationale:** Agent responses contain markdown. A small regex-based converter avoids pulling in a full markdown library.
**Alternative considered:** Pull in `marked` or `showdown` via CDN — considered but rejected to keep dependency count low; current regex approach covers the needed subset.

## Risks / Trade-offs

- **Dark theme may not appeal to all users** — Mitigated by including a light/dark toggle in the header, persisted to localStorage
- **Single-file CSS can grow unwieldy** — Mitigated by clear section organization and comment headers; can split later if needed
- **Responsive layout may break on very small screens (< 360px)** — Acknowledged; not targeting sub-360px devices
- **CDN dependencies (Vue, Element Plus, Baidu Maps)** — Existing risk, unchanged by this redesign
