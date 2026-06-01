## ADDED Requirements

### Requirement: Map API Key Environment Variable
The application SHALL use `BAIDU_MAPS_JS_AK` environment variable to configure the Baidu Maps JS API key.

#### Scenario: Environment variable is defined in .env
- **WHEN** the .env file is configured
- **THEN** `BAIDU_MAPS_JS_AK` MUST be set to a valid Baidu Maps API key

#### Scenario: Environment variable is documented in .env.example
- **WHEN** viewing .env.example
- **THEN** `BAIDU_MAPS_JS_AK` MUST be documented with description "百度地图浏览器端 AK"

### Requirement: Map API Key Runtime Replacement
The main.py application SHALL replace the placeholder `__BAIDU_MAPS_JS_AK__` in index.html with the actual API key at runtime.

#### Scenario: Placeholder exists in HTML
- **WHEN** viewing static/index.html
- **THEN** the Baidu Maps script tag MUST contain `ak=__BAIDU_MAPS_JS_AK__`

#### Scenario: Replacement occurs on root endpoint
- **WHEN** the GET / endpoint is called
- **THEN** main.py MUST read static/index.html
- **AND** MUST replace all occurrences of `__BAIDU_MAPS_JS_AK__` with `os.environ["BAIDU_MAPS_JS_AK"]`
- **AND** MUST return the modified HTML

#### Scenario: Missing API key causes error
- **WHEN** `BAIDU_MAPS_JS_AK` is not set in environment
- **THEN** the application MUST raise a ValueError at startup
- **AND** the error message MUST indicate the missing required environment variable