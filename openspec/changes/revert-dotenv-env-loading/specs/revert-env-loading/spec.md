## ADDED Requirements

### Requirement: Environment variables loaded by main.py
main.py SHALL call `load_dotenv()` at module level before any other imports that access environment variables.

#### Scenario: load_dotenv called in main.py
- **WHEN** main.py is imported/run
- **THEN** `load_dotenv()` is called before any agent module accesses environment variables

### Requirement: Agent module uses direct environment variable access
app/agents/agent.py SHALL access environment variables directly using `os.environ["KEY"]` without calling `load_dotenv()`.

#### Scenario: Agent reads env vars directly
- **WHEN** agent.py module is loaded
- **THEN** environment variables are read via `os.environ["OPENAI_API_KEY"]`, `os.environ.get("OPENAI_BASE_URL", ...)`, and `os.environ["BAIDU_MAPS_API_KEY"]`

#### Scenario: Missing env var raises KeyError
- **WHEN** OPENAI_API_KEY or BAIDU_MAPS_API_KEY is not set
- **THEN** Python raises KeyError when agent.py is imported (original behavior)
