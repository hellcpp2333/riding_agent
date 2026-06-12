## ADDED Requirements

### Requirement: Unified climb gradient color scheme
The system SHALL define a single unified color scheme for climb gradient visualization, mapped to 5 gradient ranges as specified below.

| Gradient | Hex Color | CSS Class Suffix |
|----------|-----------|-------------------|
| <3% | `#D8F5A2` | `-1` |
| 3-6% | `#F5BF2A` | `-2` |
| 6-9% | `#F98925` | `-3` |
| 9-12% | `#EE3E3E` | `-4` |
| >12% | `#B10D0D` | `-5` |

#### Scenario: All visualization layers use the same colors
- **WHEN** the frontend renders climb segment visualizations
- **THEN** the map polylines, elevation chart fills, gradient legend dots, and difficulty badges SHALL all reference the same 5 hex color values
- **AND** there SHALL be exactly one definition location for the hex values in JavaScript

#### Scenario: Color consistency across the application
- **WHEN** a climb segment with a given gradient range is displayed
- **THEN** the color shown on the map line SHALL match the color in the elevation chart for the same gradient
- **AND** the legend SHALL display the corresponding color dot
