## MODIFIED Requirements

### Requirement: Token-level streaming chat response
The system SHALL stream LLM-generated text one character at a time to the frontend, providing true character-by-character real-time display with no artificial delay.

#### Scenario: User sends a chat message and receives streaming characters
- **WHEN** user sends a message via POST /api/chat with a valid thread_id
- **THEN** the SSE response SHALL emit `token` events each containing a single character of the LLM response
- **AND** the frontend SHALL append each character to the corresponding AI message bubble incrementally
- **AND** no artificial delay SHALL be inserted between character emissions

#### Scenario: LLM invokes a tool during streaming
- **WHEN** the LLM decides to call a tool during streaming response generation
- **THEN** the SSE response SHALL emit a `tool_start` event with tool name and arguments
- **AND** the system SHALL wait for tool execution and emit `tool_result` event before resuming character streaming

#### Scenario: Streaming completes normally
- **WHEN** all characters have been emitted and tool calls are resolved
- **THEN** the SSE response SHALL emit a `done` event with the thread_id
