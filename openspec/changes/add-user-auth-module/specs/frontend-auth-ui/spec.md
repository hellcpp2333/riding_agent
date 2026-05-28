## ADDED Requirements

### Requirement: Login Page
The application SHALL display a login page when no valid authentication token is present in localStorage. The page SHALL use Element Plus components (`el-form`, `el-input`, `el-button`) and maintain consistent styling with the existing app (primary color #1890ff).

#### Scenario: Unauthenticated user visits app
- **WHEN** a user opens the application URL without a valid token in localStorage
- **THEN** the system displays the login page with username and password fields, a "登录" button, and a link to switch to the registration page

#### Scenario: Successful login redirects to main app
- **WHEN** a user enters valid credentials on the login page and clicks "登录"
- **THEN** the system stores the JWT token in localStorage, loads user info, and transitions to the cycling assistant main page

#### Scenario: Failed login shows error
- **WHEN** a user submits invalid credentials on the login page
- **THEN** the system displays an Element Plus `el-message` error notification with "用户名或密码错误"

### Requirement: Registration Page
The application SHALL display a registration page accessible via a link from the login page. The form SHALL include username (3-20 chars) and password (min 6 chars) fields with client-side validation.

#### Scenario: Successful registration
- **WHEN** a user enters a unique username and valid password on the registration page
- **THEN** the system creates the account, automatically logs the user in, stores the token, and transitions to the main page

#### Scenario: Registration validation errors
- **WHEN** a user enters a username shorter than 3 characters or password shorter than 6 characters
- **THEN** the system displays inline form validation errors using Element Plus `el-form` rules

### Requirement: User Avatar Dropdown Menu
The main application page SHALL display the user's avatar (or a default avatar if none uploaded) in the top-right corner. Clicking the avatar SHALL open an Element Plus `el-dropdown` menu with options: "个人信息" (Profile), "修改头像" (Change Avatar), and "退出登录" (Logout).

#### Scenario: Avatar displays user's uploaded image
- **WHEN** a logged-in user has uploaded a custom avatar
- **THEN** the top-right corner displays a circular avatar with the user's image URL

#### Scenario: Default avatar for new users
- **WHEN** a logged-in user has not uploaded an avatar
- **THEN** the top-right corner displays a default avatar icon with the user's username initial

#### Scenario: Profile menu item opens profile panel
- **WHEN** the user clicks "个人信息" in the avatar dropdown
- **THEN** the system displays an Element Plus dialog (`el-dialog`) showing the user's profile with editable nickname field

#### Scenario: Change avatar opens file picker
- **WHEN** the user clicks "修改头像" in the avatar dropdown
- **THEN** the system opens a file picker dialog for jpg/png images, uploads the selected file, and updates the displayed avatar

#### Scenario: Logout returns to login page
- **WHEN** the user clicks "退出登录" in the avatar dropdown
- **THEN** the system calls the logout API, clears the token from localStorage, clears user info from state, and returns to the login page

### Requirement: Protected API Calls
All API calls to `/api/chat`, `/api/route/plan`, and `/api/sessions` SHALL include the `Authorization: Bearer <token>` header when the user is authenticated. If a 401 response is received, the app SHALL redirect to the login page.

#### Scenario: Chat request includes auth header
- **WHEN** the user sends a message via the chat interface
- **THEN** the POST request to `/api/chat` includes the `Authorization: Bearer <token>` header

#### Scenario: 401 response redirects to login
- **WHEN** any protected API call returns HTTP 401
- **THEN** the system clears the token from localStorage and redirects to the login page
