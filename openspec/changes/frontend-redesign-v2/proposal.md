## Why

The current frontend is functional but visually generic — a typical "AI slop" aesthetic with default blue-on-white styling, no design personality, and no character. The `frontend-design` skill guides us toward a distinctive, memorable visual identity. A cycling route app should feel connected to the outdoors: organic, grounded, purposeful.

## What Changes

- Extract inline `<style>` to `static/css/style.css` with CSS custom properties defining an earth-toned, nature-inspired palette
- Redesign every UI surface with a cohesive aesthetic direction: organic greens, warm stone neutrals, clay terracotta accents
- Redesign auth pages with atmospheric gradient + app branding
- Polish chat bubbles, route cards, modals, and form elements with refined spacing and subtle motion
- Add map route info overlay
- **Map layout preserved**: sidebar 380px + map flex:1, BMapGL init unchanged
- No dark/light toggle, no responsive breakpoints

## Capabilities

### New Capabilities
- `earth-tone-design-system`: CSS tokens for a refined, outdoor-inspired palette
- `polished-auth`: Atmospheric branded login/register experience
- `refined-chat-routes`: Polished chat bubbles, route cards, and map overlay

### Modified Capabilities
None.

## Impact

- `static/index.html` — `<style>` → `<link>`, minor HTML additions (branding, overlay, route card icons)
- New `static/css/style.css` — design tokens, all component styles
- BMapGL init and `#map-container` CSS — byte-identical
- No backend or API changes
