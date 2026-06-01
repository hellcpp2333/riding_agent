## Context

Current frontend is a single `static/index.html` with inline `<style>` and Vue 3 + Element Plus via CDN. It violates Web Interface Guidelines in multiple areas. The sidebar+map flexbox layout is proven and must not change.

## Goals / Non-Goals

**Goals:** Extract CSS with design tokens. Fix all guideline anti-patterns. Polish visual design. Preserve map layout.
**Non-Goals:** No dark/light toggle. No responsive breakpoints. No backend changes. No new dependencies.

## Decisions

1. **Design tokens (light only)**: CSS custom properties for colors/spacing/typography. Light theme only — no runtime switching.
2. **Focus states**: Use `:focus-visible` with `box-shadow` rings on all interactive elements. Never `outline: none` without replacement.
3. **Animations**: Animate `opacity` and `transform` only. No `transition: all`. Honor `prefers-reduced-motion`.
4. **Anti-pattern fixes**: Replace all flagged patterns per Web Interface Guidelines.
5. **Map layout**: Byte-identical CSS for `.main-app`, `#sidebar`, `#map-container`, `#map`.

## Guidelines Compliance Checklist

- Focus-visible rings on buttons, inputs, nav-tabs
- Icon-only buttons: add aria-label (export, delete, theme toggle if present)
- Form inputs: autocomplete attributes, proper types
- `touch-action: manipulation` on interactive elements
- `prefers-reduced-motion` media query wraps all animations
- No `transition: all` — explicit property lists
- No `outline: none` without focus-visible replacement
- `overscroll-behavior: contain` on modals
- Button hover states throughout
- Proper ellipsis `…` in loading states
- Non-breaking spaces in units (e.g., `10 km`)
