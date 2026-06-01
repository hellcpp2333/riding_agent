## Context

Sidebar at 380px packs: header (title + nav tabs + session select + new button + avatar), chat messages, input area with placeholder text. At current width, elements overflow and text gets truncated.

## Decisions

- Widen `#sidebar` from `380px` to `440px` — gives header ~60px more breathing room
- Increase `min-width` from `320px` to `380px` — maintains minimum usable width
- No other layout changes needed

## Risks

Minimal — widening sidebar only reduces map area slightly. 440px is still reasonable for a 2-panel layout.