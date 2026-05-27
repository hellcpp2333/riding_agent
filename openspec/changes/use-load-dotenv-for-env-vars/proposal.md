## Why

The project currently has `load_dotenv()` in main.py, but `app/agents/agent.py` accesses `os.environ` at module import time (lines 20-22). This creates two problems:

1. **Race condition**: If agent.py is imported before load_dotenv() runs, environment variables will be empty
2. **No error handling**: agent.py uses `os.environ["KEY"]` which raises KeyError if missing, with no helpful message

## What Changes

- Modify `app/agents/agent.py` to call `load_dotenv()` before accessing environment variables
- Add proper error handling with configurable defaults
- Remove hard-coded API key handling from main.py if redundant

**Breaking Changes**: None (backward compatible)

## Capabilities

### New Capabilities
- **env-loading**: Centralized environment variable loading with proper error handling

### Modified Capabilities
- None (implementation detail only)

## Impact

- `app/agents/agent.py` - Primary change, add load_dotenv() call
- `main.py` - May remove redundant env var checks