## ADDED Requirements

### Requirement: GPX File Import
The system SHALL allow authenticated users to upload .gpx files, parse the track data, store the GPX file in OSS, and save metadata to MySQL.

#### Scenario: Successful GPX import
- **WHEN** a user uploads a valid `.gpx` file with track data (trk/trkseg/trkpt elements)
- **THEN** the system parses the GPX, uploads it to OSS at `routes/{user_id}/{timestamp}_{uuid}.gpx`, saves metadata to the `routes` table, and returns HTTP 201 with the parsed route summary (name, distance, elevation_gain, track_points)

#### Scenario: Invalid file format
- **WHEN** a user uploads a file that is not `.gpx` extension or not valid GPX XML
- **THEN** the system returns HTTP 400 with "仅支持 .gpx 格式" or "GPX 格式无效：{error}"

#### Scenario: File too large
- **WHEN** a user uploads a file exceeding 10MB
- **THEN** the system returns HTTP 400 with "文件大小不能超过 10MB"

### Requirement: Route List
The system SHALL allow authenticated users to list their saved routes.

#### Scenario: List user routes
- **WHEN** a user sends GET `/api/routes`
- **THEN** the system returns a JSON array of route summaries (id, name, distance, source, created_at) belonging to that user

#### Scenario: Empty list
- **WHEN** a user with no saved routes sends GET `/api/routes`
- **THEN** the system returns an empty JSON array

### Requirement: Route Detail
The system SHALL allow authenticated users to retrieve a single route's detail including track point coordinates.

#### Scenario: Get route detail
- **WHEN** a user sends GET `/api/routes/{id}` for a route they own
- **THEN** the system returns the route metadata plus the full track point array (lat, lon, ele)

#### Scenario: Route not owned by user
- **WHEN** a user sends GET `/api/routes/{id}` for a route owned by another user
- **THEN** the system returns HTTP 403

### Requirement: GPX File Export
The system SHALL allow authenticated users to download saved GPX files.

#### Scenario: Export saved route
- **WHEN** a user sends GET `/api/routes/{id}/export` for a route they own
- **THEN** the system streams the GPX file from OSS as a downloadable attachment

### Requirement: Agent-Planned Route Export
The system SHALL allow authenticated users to export an Agent-planned route as a GPX file without saving it to the database.

#### Scenario: Export agent route as GPX
- **WHEN** a user sends POST `/api/routes/export-plan` with a JSON body containing route name and coordinate array
- **THEN** the system assembles a valid GPX XML and returns it as a downloadable `.gpx` file

### Requirement: Route Deletion
The system SHALL allow authenticated users to delete their saved routes (both OSS file and DB record).

#### Scenario: Delete owned route
- **WHEN** a user sends DELETE `/api/routes/{id}` for a route they own
- **THEN** the system deletes the OSS object and the DB record, returns HTTP 204

### Requirement: Agent Route Tools
The Agent SHALL have access to tools for querying the user's saved routes and analyzing route details.

#### Scenario: Agent lists user routes
- **WHEN** a user asks the Agent "我有哪些路书"
- **THEN** the Agent calls `list_user_routes` tool, returning route summaries from the DB

#### Scenario: Agent analyzes a route
- **WHEN** a user asks the Agent to analyze a specific saved route
- **THEN** the Agent calls `get_route_detail` tool, returning distance, elevation, and sampled track points

### Requirement: Frontend Route Management View
The system SHALL provide a "路书" tab in the top navigation, containing a route management view with import button, route list, and map overlay.

#### Scenario: Import a route via UI
- **WHEN** a user clicks "导入路书" on the route management page and selects a `.gpx` file
- **THEN** the system uploads the file, displays a confirmation dialog with route summary, and upon confirmation adds the route to the list

#### Scenario: View route on map
- **WHEN** a user clicks a route card in the list
- **THEN** the system renders the track as a polyline on the Baidu Map and shows a detail panel

#### Scenario: Export route via UI
- **WHEN** a user clicks "导出" on a route card
- **THEN** the browser downloads the GPX file

#### Scenario: Delete route via UI
- **WHEN** a user clicks "删除" on a route card and confirms
- **THEN** the route is removed from the list, OSS, and DB
