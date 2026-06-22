## MODIFIED Requirements

### Requirement: Power zone legend display
The frontend SHALL display a power zone color legend overlay on the map when power-colored route segments are active, using Chinese zone labels.

| Zone | Chinese Name | Hex Color |
|------|-------------|-----------|
| Z1 | 恢复 | `#A0A0A0` |
| Z2 | 耐力 | `#3498DB` |
| Z3 | 节奏 | `#2ECC71` |
| Z4 | 阈值 | `#F1C40F` |
| Z5 | 最大摄氧量 | `#E67E22` |
| Z6 | 无氧 | `#E74C3C` |
| Z7 | 神经肌肉 | `#8E44AD` |

#### Scenario: Power-colored route is displayed
- **WHEN** the map renders power-colored route segments
- **THEN** a legend overlay SHALL appear at the bottom-left corner of the map
- **AND** the legend SHALL show 7 rows (Z1-Z7), each with a colored dot and the Chinese zone name label (恢复 / 耐力 / 节奏 / 阈值 / 最大摄氧量 / 无氧 / 神经肌肉)

#### Scenario: Map view switches away from power-colored route
- **WHEN** the user switches to a non-FIT route or clears the map
- **THEN** the power zone legend SHALL be removed from the map

#### Scenario: Legend toggle for space-constrained viewports
- **WHEN** the viewport width is less than 600px (mobile)
- **THEN** the legend SHALL collapse to show only colored dots without labels
- **OR** the legend SHALL be hidden by default with a toggle button to show/hide it
