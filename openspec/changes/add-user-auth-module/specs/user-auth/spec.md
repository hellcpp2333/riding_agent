## ADDED Requirements

### Requirement: User Registration
The system SHALL allow new users to register with a unique username and password. The password SHALL be hashed using bcrypt before storage. The username MUST be 3-20 characters and unique in the system.

#### Scenario: Successful registration
- **WHEN** a user submits a registration request with a unique username (3-20 chars) and a password (minimum 6 chars)
- **THEN** the system creates a new user record in MySQL with bcrypt-hashed password and returns HTTP 201 with the user's ID and username

#### Scenario: Duplicate username
- **WHEN** a user submits a registration request with a username that already exists
- **THEN** the system returns HTTP 409 with an error message indicating the username is taken

#### Scenario: Invalid input
- **WHEN** a user submits a registration request with username shorter than 3 characters or password shorter than 6 characters
- **THEN** the system returns HTTP 422 with validation error details

### Requirement: User Login
The system SHALL authenticate users with username and password, returning a JWT access token and storing the session in Redis with a 24-hour TTL.

#### Scenario: Successful login
- **WHEN** a user submits valid credentials (existing username and correct password)
- **THEN** the system generates a JWT token, stores the session in Redis with key `auth:session:{token}`, sets user online status in Redis, and returns HTTP 200 with the token, user info (id, username, nickname, avatar_url)

#### Scenario: Invalid credentials
- **WHEN** a user submits a login request with a non-existent username or incorrect password
- **THEN** the system returns HTTP 401 with a generic error message "用户名或密码错误"

### Requirement: User Logout
The system SHALL allow authenticated users to log out by invalidating their session token in Redis.

#### Scenario: Successful logout
- **WHEN** an authenticated user sends a POST request to `/api/auth/logout` with a valid Bearer token
- **THEN** the system removes the session from Redis, sets user status to offline, and returns HTTP 200

#### Scenario: Logout with expired token
- **WHEN** a user sends a logout request with an expired or invalid token
- **THEN** the system returns HTTP 401

### Requirement: Token Verification Middleware
All protected API endpoints (`/api/chat`, `/api/route/plan`) SHALL require a valid JWT token in the `Authorization: Bearer <token>` header. The middleware SHALL verify the JWT signature and check that the session exists in Redis.

#### Scenario: Valid token on protected endpoint
- **WHEN** a request to `/api/chat` includes a valid, non-expired JWT token that has an active session in Redis
- **THEN** the request proceeds and the current user info is available via `Depends(get_current_user)`

#### Scenario: Missing token on protected endpoint
- **WHEN** a request to `/api/chat` is made without an `Authorization` header
- **THEN** the system returns HTTP 401 with "未登录"

#### Scenario: Expired token on protected endpoint
- **WHEN** a request to `/api/chat` includes an expired JWT token
- **THEN** the system returns HTTP 401 with "登录已过期"

#### Scenario: Token revoked (logged out) on protected endpoint
- **WHEN** a request to `/api/chat` includes a JWT token whose session has been removed from Redis
- **THEN** the system returns HTTP 401 with "登录已失效"

### Requirement: Health Check Endpoint
The system SHALL provide an unauthenticated `/api/auth/me` endpoint that returns current user info when authenticated, or HTTP 401 when not.

#### Scenario: Authenticated user checks status
- **WHEN** a user sends GET `/api/auth/me` with a valid Bearer token
- **THEN** the system returns HTTP 200 with user info (id, username, nickname, avatar_url)

#### Scenario: Unauthenticated user checks status
- **WHEN** a user sends GET `/api/auth/me` without a token
- **THEN** the system returns HTTP 401
