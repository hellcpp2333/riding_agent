## Why

Current frontend is functional but visually unpolished — a single monolithic HTML file with raw inline CSS, no design system, minimal spacing/typography hierarchy, and no visual feedback or transitions. A redesign will make the app feel professional, modern, and pleasant to use, which matters for a consumer-facing cycling tool.

## What Changes

- Extract CSS into a standalone stylesheet with CSS custom properties (design tokens)
- Establish a cohesive color palette and typography system
- Add smooth transitions, hover effects, and micro-interactions
- Redesign the auth pages with a more polished layout and better visual hierarchy
- Modernize the chat UI — improved message bubbles, better spacing, typing indicators
- Redesign the route management view with card-based layout and empty-state illustrations
- Improve the sidebar/navigation with consistent spacing and active-state indicators
- Add responsive design for mobile/tablet viewports
- Dark color scheme for better readability in outdoor cycling contexts
- Keep Element Plus as the UI framework but apply consistent theming

## Capabilities

### New Capabilities
- `frontend-design-system`: Cohesive CSS design system with tokens (colors, spacing, typography, shadows, radii)
- `responsive-layout`: Mobile/tablet-responsive layout adapting sidebar and map
- `polished-auth-ui`: Redesigned login/register pages with improved visual hierarchy
- `modern-chat-ui`: Refined chat interface with smooth animations, better message rendering, typing indicator
- `route-management-ui`: Polished route cards with improved layout, empty state, and interactions

### Modified Capabilities
None — existing API capabilities remain unchanged; this is a pure UI refresh.

## Impact

- `static/index.html` — complete rewrite of the HTML structure, keeping Vue 3 + Element Plus CDN
- New `static/css/` directory — extracted stylesheets
- No backend changes, no API changes, no new dependencies
- Existing functionality preserved — all features continue to work identically
