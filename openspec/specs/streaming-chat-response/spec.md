## ADDED Requirements

### Requirement: Token-level streaming chat response
The system SHALL stream LLM-generated text tokens to the frontend in real-time, allowing users to read the assistant's response as it is being generated, rather than waiting for the full response.

#### Scenario: User sends a chat message and receives streaming tokens
- **WHEN** user sends a message via POST /api/chat with a valid thread_id
- **THEN** the SSE response SHALL emit `token` events with partial text content as the LLM generates it
- **AND** the frontend SHALL append each token to the corresponding AI message bubble incrementally

#### Scenario: LLM invokes a tool during streaming
- **WHEN** the LLM decides to call a tool during streaming response generation
- **THEN** the SSE response SHALL emit a `tool_start` event with tool name and arguments
- **AND** the system SHALL wait for tool execution and emit `tool_result` event before resuming token streaming

#### Scenario: Streaming completes normally
- **WHEN** all LLM tokens have been emitted and tool calls are resolved
- **THEN** the SSE response SHALL emit a `done` event with the thread_id

### Requirement: Backward compatible streaming events
The system SHALL maintain all existing SSE event types (`route`, `elevation`, `tool_start`, `tool_result`) alongside the new `token` events.

#### Scenario: Existing route and elevation events still work
- **WHEN** a `map_directions` tool result is processed
- **THEN** the SSE response SHALL emit `route` and `elevation` events exactly as before
- **AND** the frontend SHALL continue to render route lines and elevation charts from these events
