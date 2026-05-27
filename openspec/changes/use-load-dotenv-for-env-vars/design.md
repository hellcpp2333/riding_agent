## Context

Currently `load_dotenv()` is called in main.py, but `app/agents/agent.py` imports at the top level:
- `OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]` (line 20)
- `OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com")` (line 21)
- `BAIDU_MAPS_API_KEY = os.environ["BAIDU_MAPS_API_KEY"]` (line 22)

This means these values are read when agent.py is first imported, BEFORE main.py's load_dotenv() runs.

## Goals / Non-Goals

**Goals:**
- Fix env var loading timing issue
- Add proper error handling with helpful messages
- Keep backward compatibility with existing .env files

**Non-Goals:**
- Don't change existing behavior (API endpoints, LLM calls)
- Don't add new configuration sources

## Decisions

1. **Call load_dotenv() in agent.py**: Add `from dotenv import load_dotenv; load_dotenv()` at the top of agent.py before accessing os.environ
2. **Add error handling**: Use try/except to provide helpful error messages when required env vars are missing
3. **Lazy evaluation**: Consider using lazy property or function to defer env var access until actually needed

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Multiple load_dotenv() calls | python-dotenv is safe to call multiple times, only first load takes effect |
| .env file not found | Default to empty string, show warning but don't crash |

## Migration Plan

1. Add load_dotenv() to agent.py
2. Test that app starts correctly
3. Remove redundant env handling from main.py if any