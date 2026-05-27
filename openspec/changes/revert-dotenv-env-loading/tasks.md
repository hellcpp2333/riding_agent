## 1. Revert agent.py Changes

- [x] 1.1 Remove `from dotenv import load_dotenv; load_dotenv()` from top of agent.py
- [x] 1.2 Restore original `os.environ["KEY"]` access pattern for env vars
- [x] 1.3 Remove error handling wrapper for env var checks

## 2. Restore main.py Original State

- [x] 2.1 Add back `from dotenv import load_dotenv; load_dotenv()` at top of main.py
- [x] 2.2 Restore `BAIDU_MAPS_API_KEY` environment variable reading and warning
