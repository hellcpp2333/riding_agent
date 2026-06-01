## ADDED Requirements

### Requirement: Refined message bubbles
Chat messages SHALL use distinct, polished bubble styles for user and assistant roles with proper spacing and rounded corners.

#### Scenario: User message styling
- **WHEN** a user message is displayed
- **THEN** it appears right-aligned with `--color-primary` background, white text, 12px border-radius (4px on bottom-right), and 6px bottom margin

#### Scenario: Assistant message styling
- **WHEN** an assistant message is displayed
- **THEN** it appears left-aligned with `--color-surface-secondary` background, 12px border-radius (4px on bottom-left), 1px border, and 6px bottom margin

#### Scenario: Message content formatting
- **WHEN** agent response contains markdown (bold, italic, code, lists, links)
- **THEN** the content is rendered with appropriate HTML formatting using the helper function

### Requirement: Tool call and status indicators
The system SHALL display visual indicators when tools are being invoked by the agent.

#### Scenario: Tool invocation indicator
- **WHEN** the agent starts calling a tool
- **THEN** a subtle pulsing indicator appears in the chat showing the tool name (e.g., "正在查询地图...")

#### Scenario: Route data card in messages
- **WHEN** agent response includes route data
- **THEN** a visually distinct route summary card (with distance, duration, and a route icon) is displayed within the assistant message

### Requirement: Auto-scroll behavior
The chat container SHALL auto-scroll to the latest message when new content appears, unless the user has manually scrolled up to read history.

#### Scenario: Auto-scroll on new message
- **WHEN** a new message or token is appended
- **THEN** the chat container scrolls to the bottom if the user was already at the bottom (within 100px of bottom)

#### Scenario: Respect manual scroll
- **WHEN** user has scrolled up more than 100px from the bottom
- **THEN** auto-scroll is suppressed until the user scrolls back to the bottom

### Requirement: Send button and input states
The message input area SHALL provide clear visual feedback for input focus, empty state, and sending state.

#### Scenario: Input focus state
- **WHEN** the message input receives focus
- **THEN** the border color changes to `--color-primary` with a subtle glow shadow

#### Scenario: Send button disabled
- **WHEN** the input is empty or whitespace-only
- **THEN** the send button shows reduced opacity (0.5) and `cursor: not-allowed`

#### Scenario: Sending state
- **WHEN** a message is being sent
- **THEN** the send button shows a loading spinner and the input is disabled
