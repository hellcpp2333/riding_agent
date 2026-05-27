## ADDED Requirements

### Requirement: Environment variables loaded from .env file
The system SHALL load all environment variables from a `.env` file at application startup using `python-dotenv`.

#### Scenario: Application starts with .env file
- **WHEN** the application starts
- **THEN** `load_dotenv()` is called before any environment variable is accessed

### Requirement: Required environment variables validated
The system SHALL validate that all required environment variables are present at startup and provide clear error messages if any are missing.

#### Scenario: All required variables present
- **WHEN** all required environment variables (OPENAI_API_KEY, BAIDU_MAPS_API_KEY) are set
- **THEN** the application starts normally

#### Scenario: Missing required variable
- **WHEN** a required environment variable is missing
- **THEN** the application fails to start with a clear error message indicating which variable is missing

### Requirement: .env.example template provided
The system SHALL provide a `.env.example` file documenting all required and optional environment variables.

#### Scenario: New developer setup
- **WHEN** a new developer clones the repository
- **THEN** they can copy `.env.example` to `.env` and fill in their credentials

### Requirement: API credentials not hardcoded
The system SHALL NOT contain hardcoded API keys or base URLs in source code.

#### Scenario: Reviewing source code
- **WHEN** examining the application source code
- **THEN** no API keys or secrets are visible in any `.py` files
