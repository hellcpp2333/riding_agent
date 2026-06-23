## Context

The previous fix (600px canvas, 1600px modal, wider ticks) didn't fully resolve the user's complaint about cadence/speed expanded charts being too small and dense. The user explicitly wants the expanded design to match the original power chart expanded view.

## Goals / Non-Goals

**Goals:**
- Much larger expanded canvas (750px) and modal (1800px)
- More breathing room via larger padding
- Cleaner lines via more aggressive downsampling
- Readable labels via larger fonts and more Y-axis ticks

**Non-Goals:**
- No per-chart-type customization (uniform improvements)
- No changes to inline (non-expanded) charts

## Decisions

### 1. Canvas: 600px → 750px, Modal: 1600px → 1800px

25% taller and 12.5% wider than the previous fix. Gives cadence/speed data enough vertical space to show fluctuations clearly.

### 2. Downsampling: 2000 → 1000 points

Half the data points means smoother, less "noisy" looking lines. For a 2-hour ride, 1000 points = one point every 7.2 seconds — still well above the Nyquist rate for cycling data (cadence/speed sensors record at ~1Hz).

### 3. Padding: `{t:20, r:24, b:48, l:60}` → `{t:30, r:30, b:56, l:72}`

Larger padding gives the chart more breathing room, matching the airy feel of the original power expanded chart.

### 4. Fonts: Y-axis 12→14px, X-axis 11→12px

Larger fonts improve readability on the bigger canvas.

### 5. Y-axis ticks: 6 → 8

More grid lines give finer value reference, useful for speed (typically 0-50 km/h) and cadence (0-120 rpm) where smaller value differences matter.

## Risks / Trade-offs

- Fewer downsampled points could miss short-duration peaks. Mitigation: 1000 points for a 30-minute ride = one every 1.8 seconds — sufficient to capture 5-second power/cadence spikes.
