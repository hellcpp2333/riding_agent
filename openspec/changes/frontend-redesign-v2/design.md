## Context

Single-file frontend with Vue 3 + Element Plus + BMapGL CDN. The `frontend-design` skill guides us toward a **refined, organic aesthetic** inspired by the outdoors — cycling is about nature, earth, trail.

## Aesthetic Direction

**Organic / Refined — Earth-toned cycling explorer**

- **Color**: Sage green primary, warm stone backgrounds, terracotta clay accents, off-white cards
- **Typography**: Refined system font stack with generous letter-spacing on headings, tabular numbers for stats
- **Motion**: Subtle. Cards lift on hover. Messages fade in. Route data appears with staggered timing. No gratuitous animation.
- **Composition**: Sidebar breathes. Generous padding. Cards have air. The map dominates — routes bloom in rich green.
- **What makes it unforgettable**: It doesn't look like a generic SaaS dashboard. It feels purpose-built for cycling — warm, grounded, natural.

## Goals / Non-Goals

**Goals:** Distinctive earth-tone palette, refined sidebar, map-first layout, subtle motion, BMapGL works unchanged.
**Non-Goals:** Dark mode, responsive breakpoints, new dependencies, backend changes.

## Decisions

1. **Earth-tone palette**: Sage green (#3a7d44) primary, warm stone (#f5f0e8) bg, clay terracotta (#c4734f) accent. CSS custom properties.
2. **Map layout preserved exactly**: `#sidebar { width: 380px }`, `#map-container { flex: 1 }` — byte-identical to original.
3. **Single stylesheet**: `static/css/style.css` with organized sections.
4. **Subtle transitions**: Opacity + transform only, 200ms duration, prefers-reduced-motion respected.
5. **Element Plus overridden**: Form components themed to match earth-tone palette.
