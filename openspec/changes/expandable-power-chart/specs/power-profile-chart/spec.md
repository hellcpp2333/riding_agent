## ADDED Requirements

### Requirement: Expandable power chart modal
The power profile chart section SHALL include an expand button that opens a full-width modal for detailed viewing, referencing Garmin Connect's chart expansion pattern.

#### Scenario: User clicks expand button
- **WHEN** user clicks the expand button (⊕ icon) in the top-right corner of the power profile chart section
- **THEN** a modal overlay SHALL open displaying an enlarged version of the power profile chart
- **AND** the modal SHALL occupy 90vw width with a maximum of 1200px
- **AND** the modal SHALL have a close button (✕) in the top-right corner

#### Scenario: User closes the modal
- **WHEN** user clicks the close button or the modal backdrop
- **THEN** the modal SHALL close
- **AND** the original chart in the sidebar SHALL remain unchanged

#### Scenario: Expanded chart X-axis detail
- **WHEN** the power chart is rendered in the expanded modal
- **THEN** the X-axis SHALL display time labels at ~5 minute intervals (or denser for shorter rides)
- **AND** the chart height SHALL be at least 400px for better vertical resolution
- **AND** the number of data points rendered SHALL be up to 2000 (vs 1000 in the mini chart)

#### Scenario: No power data available
- **WHEN** the activity has no power profile data
- **THEN** the expand button SHALL NOT be displayed (since the chart section itself is hidden)
