## ADDED Requirements

### Requirement: Expanded chart sizing

The expanded chart modal SHALL render with a 750px canvas height and 1800px modal max-width. The plot area SHALL use padding of {top:30, right:30, bottom:56, left:72}. Y-axis SHALL display 8 grid lines with 14px font labels. X-axis SHALL display time labels with 12px font. Data SHALL be downsampled to at most 1000 points.

#### Scenario: All expanded charts match power chart design
- **WHEN** any expanded chart (power, speed, HR, cadence, elevation) opens
- **THEN** the canvas SHALL be 750px tall
- **THEN** the modal SHALL be up to 1800px wide
- **THEN** the plot area SHALL use padding {t:30, r:30, b:56, l:72}
- **THEN** Y-axis SHALL have 8 grid lines with 14px labels
- **THEN** X-axis SHALL have 12px time labels
- **THEN** data SHALL contain at most 1000 points

#### Scenario: Clean line rendering
- **WHEN** a cadence or speed expanded chart renders with high-frequency sensor data
- **THEN** the downsampled line SHALL appear smooth without visual noise
