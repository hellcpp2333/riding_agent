## Context

**Current State:**
- Frontend is in `static/index.html` with all CSS inline in a `<style>` block
- Visual appearance is plain with minimal styling and no design system
- Baidu Maps JS API key uses placeholder `__BAIDU_MAPS_JS_AK__` which gets replaced at runtime by `main.py`
- The map loading issue is actually handled correctly by `main.py` - the placeholder replacement mechanism works as intended

**Constraints:**
- Must preserve all existing functionality (no behavior changes)
- Must keep Vue 3 + Element Plus CDN setup
- Must maintain Baidu Maps BMapGL integration
- Design should be suitable for outdoor/cycling use context
- No new external CSS frameworks beyond Element Plus

**Stakeholders:**
- End users: cyclists who need reliable route planning and visualization
- Development team: maintainable code with clear structure

## Goals / Non-Goals

**Goals:**
- Extract inline CSS into a standalone stylesheet (`static/css/style.css`)
- Establish a cohesive design system with CSS custom properties (design tokens)
- Improve visual hierarchy, spacing, and overall aesthetics
- Ensure map continues to load correctly (verify existing mechanism works)
- Create a more professional, trustworthy appearance

**Non-Goals:**
- Changing the underlying technology stack (Vue 3, Element Plus remain)
- Adding new features or capabilities
- Modifying backend or API behavior
- Creating a dark mode or theme switching system
- Implementing responsive design for mobile/tablet

## Decisions

### 1. Design System Architecture

**Decision:** Use CSS custom properties (CSS variables) as design tokens defined in `:root` selector.

**Rationale:**
- Native browser support, no build step required
- Easy to maintain and modify globally
- Enables consistent theming across components
- Zero dependency overhead

**Alternatives considered:**
- CSS-in-JS: Would require additional dependencies and build tools
- SASS/SCSS: Would add build complexity, overkill for this scope
- Tailwind CSS: Would require build step, larger bundle size

### 2. Color Palette

**Decision:** Use an "earth-tone" palette inspired by cycling/nature with good contrast.

**Rationale:**
- Fits the outdoor/cycling use case
- Warm, organic feel is pleasant for extended use
- Good color contrast for readability

**Primary colors:**
- Primary: `#3a7d44` (forest green - nature, cycling trails)
- Background: `#f5f0e8` (warm cream)
- Surface: `#fefcf8` (near-white)
- Text: `#2c2416` (dark brown for better contrast than pure black)

### 3. Typography System

**Decision:** Use system font stack with predefined size scale.

**Rationale:**
- No external font dependency means faster load times
- System fonts are optimized for readability
- Consistent sizing scale ensures visual harmony

**Font sizes:** 12px, 13px, 14px, 16px, 18px, 22px

### 4. Map API Key Verification

**Decision:** Keep existing placeholder mechanism - verify it's working correctly.

**Rationale:**
- The current `main.py` implementation already handles API key replacement
- `__BAIDU_MAPS_JS_AK__` placeholder gets replaced with `os.environ["BAIDU_MAPS_JS_AK"]`
- No code changes needed if environment variable is set correctly

**Verification step:** Ensure `.env` has `BAIDU_MAPS_JS_AK` set to a valid key

## Risks / Trade-offs

### Risk 1: Map fails to load due to API key issue
- **Mitigation:** The existing replacement mechanism in `main.py` is sound. Ensure `.env` is properly configured with valid `BAIDU_MAPS_JS_AK`.

### Risk 2: Design changes introduce visual bugs
- **Mitigation:** Test all user flows (login, chat, route planning, route management) after changes.

### Risk 3: Inline styles removed but some dynamic styles were important
- **Mitigation:** Carefully review all inline styles during extraction; preserve any critical dynamic styles.

### Trade-off: No dark mode
- Accepting no dark mode keeps the implementation simple and focused. Dark mode could be a future enhancement.

## Migration Plan

1. Create `static/css/style.css` with design system tokens and component styles
2. Update `static/index.html` to:
   - Remove inline `<style>` block
   - Add `<link rel="stylesheet" href="/static/css/style.css">`
3. Verify `.env` has correct `BAIDU_MAPS_JS_AK` value
4. Test all major user flows:
   - Login/register
   - Chat with route planning
   - Route management (import, view, export, delete)
   - Map rendering
5. No rollback strategy needed - changes are limited to frontend CSS

## Open Questions

None - the scope is well-defined and dependencies are minimal.