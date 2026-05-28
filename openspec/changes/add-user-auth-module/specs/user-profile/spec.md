## ADDED Requirements

### Requirement: View User Profile
Authenticated users SHALL be able to retrieve their own profile information including username, nickname, and avatar URL via a GET endpoint.

#### Scenario: User views their own profile
- **WHEN** an authenticated user sends GET `/api/user/profile` with a valid Bearer token
- **THEN** the system returns HTTP 200 with the user's id, username, nickname, avatar_url, created_at, and updated_at

#### Scenario: Unauthenticated user attempts to view profile
- **WHEN** a request to `/api/user/profile` is made without a valid token
- **THEN** the system returns HTTP 401

### Requirement: Update User Profile
Authenticated users SHALL be able to update their nickname (1-20 characters). The username SHALL NOT be changeable after registration.

#### Scenario: Successful nickname update
- **WHEN** an authenticated user sends PUT `/api/user/profile` with a JSON body containing a valid nickname (1-20 chars)
- **THEN** the system updates the nickname in MySQL and returns HTTP 200 with the updated user profile

#### Scenario: Invalid nickname
- **WHEN** a user sends a PUT `/api/user/profile` request with a nickname longer than 20 characters
- **THEN** the system returns HTTP 422 with validation error details

### Requirement: Upload Avatar
Authenticated users SHALL be able to upload a profile picture (jpg/png, max 5MB) which SHALL be uploaded to Alibaba Cloud OSS (endpoint: oss-cn-shenzhen.aliyuncs.com) and the public URL SHALL be stored in MySQL `avatar_url`.

#### Scenario: Successful avatar upload
- **WHEN** an authenticated user uploads a valid jpg or png image file under 5MB to `POST /api/user/avatar`
- **THEN** the system uploads the file to OSS with key `avatars/{user_id}/{timestamp}_{random}.{ext}`, updates the user's `avatar_url` in MySQL, and returns HTTP 200 with the new avatar URL

#### Scenario: Invalid file type
- **WHEN** a user uploads a file that is not jpg or png
- **THEN** the system returns HTTP 400 with "仅支持 jpg/png 格式"

#### Scenario: File too large
- **WHEN** a user uploads a file larger than 5MB
- **THEN** the system returns HTTP 400 with "文件大小不能超过 5MB"

#### Scenario: No avatar uploaded yet
- **WHEN** a user's profile is viewed and they have never uploaded an avatar
- **THEN** the `avatar_url` field SHALL be null and the frontend SHALL display a default avatar
