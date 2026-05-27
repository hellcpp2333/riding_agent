## 1. Create .env.example Template

- [x] 1.1 Create `.env.example` file with all required and optional environment variables documented

## 2. Update main.py

- [x] 2.1 Keep `load_dotenv()` call at the top of main.py
- [x] 2.2 Add `check_required_env_vars()` function to validate required environment variables at startup
- [x] 2.3 Update `BAIDU_MAPS_API_KEY` check to use the centralized validation

## 3. Update agent.py

- [x] 3.1 Ensure agent.py reads all API keys and base URLs from environment variables only
- [x] 3.2 Remove any hardcoded fallback values for sensitive configuration

## 4. Testing

- [x] 4.1 Test application starts successfully with all required env vars set
- [x] 4.2 Test application fails gracefully with clear error when required env var is missing
