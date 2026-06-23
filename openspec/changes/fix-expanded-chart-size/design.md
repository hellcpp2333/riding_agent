## Context

The `drawTimeSeriesChartExpanded` shared function renders all expanded chart types with identical canvas dimensions (480px height) and X-axis tick intervals. Cadence and speed data naturally fluctuate more frequently than power, making the expanded view feel cramped and the X-axis labels appear too dense.

## Goals / Non-Goals

**Goals:**
- Make expanded charts larger (600px canvas height, 1600px modal width)
- Reduce X-axis tick density (wider time intervals)
- Apply uniformly to all 5 chart types

**Non-Goals:**
- No changes to the inline (non-expanded) chart rendering
- No per-chart-type customization needed

## Decisions

### 1. Canvas height: 480px → 600px

Reason: 25% taller gives cadence/speed charts more vertical room to breathe. The taller aspect ratio better suits time-series data with high-frequency fluctuations.

### 2. Modal max-width: 1400px → 1600px

Reason: Wider panel gives more horizontal space for long-duration rides, reducing perceived X-axis crowding.

### 3. X-axis tick intervals: wider minimum

Old: `totalMin > 180 ? 15 : totalMin > 60 ? 10 : totalMin > 30 ? 5 : 2`
New: `totalMin > 240 ? 20 : totalMin > 120 ? 15 : totalMin > 60 ? 10 : totalMin > 30 ? 5 : 5`

Changes:
- Min interval: 2min → 5min (halves tick count on short rides)
- 30-60min: still 5min intervals
- 60-120min: still 10min intervals  
- 120-240min: 15min intervals
- 240min+: 20min intervals

This reduces tick density while keeping labels readable and well-spaced.

## Risks / Trade-offs

- Wider intervals mean fewer reference points for very short activities (<30min). Mitigation: 5-minute intervals still give 6+ ticks for a 30min ride — sufficient for orientation.
