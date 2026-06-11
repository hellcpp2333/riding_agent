## ADDED Requirements

### Requirement: Markdown table rendering in chat
The system SHALL render Markdown tables in chat messages as HTML tables.

#### Scenario: Simple table with header and rows
- **WHEN** an AI message contains a Markdown table like `| Name | Value |\n|------|-------|\n| A | 1 |`
- **THEN** the frontend SHALL render it as an HTML `<table>` with proper header and data rows

#### Scenario: Table within a message with other content
- **WHEN** a message contains text paragraphs before and after a Markdown table
- **THEN** the table SHALL be rendered inline within the message flow
- **AND** surrounding text SHALL render normally

#### Scenario: Invalid Markdown table
- **WHEN** table syntax is malformed (missing separators, inconsistent columns)
- **THEN** the system SHALL display the raw text as-is without breaking the message layout
