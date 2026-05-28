## 1. Dependencies and Environment

- [x] 1.1 Add new Python dependencies to `pyproject.toml`: `aiomysql`, `sqlalchemy>=2.0`, `redis`, `PyJWT`, `passlib[bcrypt]`, `oss2`
- [x] 1.2 Run `uv sync` to install new dependencies
- [x] 1.3 Add MySQL and Redis environment variables to `.env.example`: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `JWT_SECRET_KEY`, `OSS_ACCESS_KEY_ID`, `OSS_ACCESS_KEY_SECRET`, `OSS_BUCKET_NAME`, `OSS_ENDPOINT`

## 2. Database Layer (MySQL)

- [x] 2.1 Create `app/db_mysql.py` with async SQLAlchemy engine/session factory and `init_db()` function that auto-creates the `users` table
- [x] 2.2 Define the `User` SQLAlchemy model in `app/models.py` with fields: id, username, password_hash, avatar_url, nickname, created_at, updated_at
- [x] 2.3 Update `main.py` lifespan to initialize MySQL connection pool and run `init_db()` on startup, dispose on shutdown

## 3. Redis Layer

- [x] 3.1 Create `app/redis_client.py` with async Redis connection pool initialization and helper functions for session management (`create_session`, `get_session`, `delete_session`, `set_user_status`, `get_user_status`)
- [x] 3.2 Update `main.py` lifespan to initialize Redis connection pool on startup and close on shutdown

## 4. Authentication API

- [x] 4.1 Create `app/auth/__init__.py` and `app/auth/schemas.py` with Pydantic models for `LoginRequest`, `RegisterRequest`, `AuthResponse`, `UserProfile`, `UpdateProfileRequest`
- [x] 4.2 Create `app/auth/utils.py` with JWT token generation (`create_access_token`), JWT verification (`decode_token`), and password hashing (`hash_password`, `verify_password`)
- [x] 4.3 Create `app/auth/dependencies.py` with `get_current_user` FastAPI dependency that extracts and validates JWT from Authorization header, checks Redis session
- [x] 4.4 Create `app/auth/routes.py` with endpoints: `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`
- [x] 4.5 Register auth router in `app/api/v1/__init__.py` or directly in `main.py`

## 5. User Profile API

- [x] 5.1 Create `app/services/oss_service.py` with async upload function that uploads to Alibaba Cloud OSS and returns public URL
- [x] 5.2 Create `app/api/v1/user_routes.py` with endpoints: `GET /api/user/profile`, `PUT /api/user/profile`, `POST /api/user/avatar` (all protected with `get_current_user`)
- [x] 5.3 Add avatar upload endpoint with file validation (jpg/png, max 5MB) and OSS upload

## 6. Protect Existing APIs

- [x] 6.1 Update `app/api/v1/routes.py` to add `Depends(get_current_user)` to `/api/chat`, `/api/route/plan`, `/api/sessions`, and `POST /api/sessions` endpoints
- [x] 6.2 Update chat and route plan handlers to use user info from `get_current_user` for personalization

## 7. Frontend Authentication UI

- [x] 7.1 Rewrite `static/index.html` to include Vue 3 + Element Plus CDN scripts and create a login/registration view with `el-form` components
- [x] 7.2 Implement login form that calls `POST /api/auth/login`, stores token in localStorage, and transitions to main app view
- [x] 7.3 Implement registration form that calls `POST /api/auth/register`, auto-logs in, and transitions to main app view
- [x] 7.4 Add user avatar dropdown in top-right corner of main page using `el-dropdown` with menu items: 个人信息, 修改头像, 退出登录
- [x] 7.5 Implement profile dialog (`el-dialog`) with editable nickname and save functionality
- [x] 7.6 Implement avatar upload with file picker, calls `POST /api/user/avatar`, and updates displayed avatar
- [x] 7.7 Add logout flow that calls `POST /api/auth/logout`, clears localStorage, and returns to login page
- [x] 7.8 Add Authorization header interceptor for all API fetch calls; on 401 response, redirect to login page
- [x] 7.9 On app load, check localStorage for existing token, call `GET /api/auth/me` to validate, auto-redirect to login if invalid

## 8. Testing and Verification

- [ ] 8.1 Test registration flow: register new user, verify user created in MySQL, verify auto-login
- [ ] 8.2 Test login flow: login with valid credentials, verify token received; login with wrong password, verify 401
- [ ] 8.3 Test protected API: call `/api/chat` without token (expect 401), call with valid token (expect success)
- [ ] 8.4 Test logout: login, logout, verify token no longer works on protected endpoints
- [ ] 8.5 Test avatar upload: upload jpg file, verify OSS URL returned and displayed in avatar
- [ ] 8.6 Test profile update: change nickname, verify saved in MySQL and displayed
- [ ] 8.7 Test full app flow: login -> chat -> plan route -> view profile -> logout -> re-login
