## ADDED Requirements

### Requirement: Message bubble styling
Chat messages SHALL use distinct, polished bubble styles for user and assistant roles with consistent spacing and rounded corners.

#### Scenario: User message bubble
- **WHEN** a user message is displayed
- **THEN** it SHALL be right-aligned with a colored background, white text, and appropriate border-radius

#### Scenario: Assistant message bubble
- **WHEN** an assistant message is displayed
- **THEN** it SHALL be left-aligned with a light background, border, and appropriate border-radius

#### Scenario: Message fade-in
- **WHEN** a new message appears
- **THEN** it SHALL animate in with a brief opacity + transform transition

### Requirement: Tool call indicator
The system SHALL display a visual indicator when the agent is invoking a tool.

#### Scenario: Tool invocation
- **WHEN** the agent calls a tool
- **THEN** a pulsing indicator SHALL appear in the chat showing the tool name

### Requirement: Input area focus
The message input SHALL provide clear visual feedback on focus and during sending.

#### Scenario: Input focus glow
- **WHEN** the input receives focus
- **THEN** the border SHALL glow with the primary color

#### Scenario: Send button states
- **WHEN** the input is empty OR a message is being sent
- **THEN** the send button SHALL show a disabled or loading state
