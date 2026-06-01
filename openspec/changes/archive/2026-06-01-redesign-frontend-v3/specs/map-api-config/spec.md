## ADDED Requirements

### Requirement: Map API Key Environment Variable
The application SHALL use `BAIDU_MAPS_JS_AK` environment variable for the Baidu Maps JS API key.

#### Scenario: Key is set in .env
- **WHEN** the .env file is configured
- **THEN** `BAIDU_MAPS_JS_AK` MUST be set to a valid key

### Requirement: Runtime Key Replacement
`main.py` SHALL replace the placeholder with the actual key at runtime.

#### Scenario: Placeholder replacement
- **WHEN** `GET /` is called
- **THEN** `__BAIDU_MAPS_JS_AK__` MUST be replaced with `os.environ["BAIDU_MAPS_JS_AK"]`
- **AND** the returned HTML MUST contain the actual key in the script src