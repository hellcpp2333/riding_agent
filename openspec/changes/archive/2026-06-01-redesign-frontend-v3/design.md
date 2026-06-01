## Context

- Frontend: inline CSS in `<style>` block, plain appearance
- Tech: Vue 3 + Element Plus CDN, BMapGL
- Map AK uses `__BAIDU_MAPS_JS_AK__` placeholder replaced at runtime by `main.py`
- No build tools — plain HTML/CSS/JS

## Goals / Non-Goals

**Goals:** Extract CSS to standalone file, apply cohesive design tokens, improve visual quality, ensure map works.

**Non-Goals:** No behavior changes, no new dependencies, no responsive/mobile, no dark mode.

## Decisions

### CSS Design Tokens
Use `:root` CSS custom properties for colors, spacing, typography, radii, shadows. Zero build dependency.

### Earth-tone Palette
Primary: `#3a7d44` (forest green), Background: `#f5f0e8` (warm cream), Surface: `#fefcf8`, Text: `#2c2416` (dark brown). Fits outdoor cycling context.

### Static File Serving
Add `app.mount("/static", StaticFiles(directory="static"), name="static")` in `main.py` to serve CSS. Must be added before route includes.

### Map API Key
Keep existing `main.py` replacement mechanism — no changes needed beyond verifying `.env` has `BAIDU_MAPS_JS_AK` set.

## Risks / Trade-offs

- **CSS conflict with Element Plus**: Mitigated by `!important` overrides
- **Cache issues**: Mitigated by new file path, versioned if needed later
- **No dark mode**: Accepted trade-off for simplicity

## Migration Plan

1. Create `static/css/style.css`
2. Update `static/index.html` (remove `<style>`, add CSS link)
3. Update `main.py` (add StaticFiles mount)
4. Verify `.env` has `BAIDU_MAPS_JS_AK`
5. Start server, test all flows