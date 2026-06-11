## ADDED Requirements

### Requirement: Local SRTM DEM elevation provider
The system SHALL provide a local SRTM elevation provider that reads HGT format tiles from disk, performs bilinear interpolation, and serves as the primary elevation source, falling back to Open Elevation API for uncovered regions.

#### Scenario: Query elevation for a single coordinate
- **WHEN** elevation is requested for a (lat, lon) coordinate
- **THEN** the system SHALL locate the corresponding SRTM HGT tile file
- **AND** perform bilinear interpolation using the surrounding 4 grid cells
- **AND** return the interpolated elevation in meters

#### Scenario: Bulk query for route points
- **WHEN** a list of route coordinate points is provided
- **THEN** the system SHALL query all points against the local DEM
- **AND** return elevation data for every point without sampling or batching limits
- **AND** complete within 500ms for up to 10,000 points

#### Scenario: Tile not available locally
- **WHEN** the required SRTM tile does not exist in `data/srtm/`
- **THEN** the system SHALL fall back to Open Elevation API for those coordinates
- **AND** log a warning indicating which tiles are missing

### Requirement: HGT binary format support
The system SHALL read SRTM HGT files directly in binary format (3601×3601 grid, int16 big-endian) without requiring GDAL or rasterio dependencies.

#### Scenario: Load HGT tile from disk
- **WHEN** a HGT file exists for the requested 1°×1° region
- **THEN** the system SHALL parse the 3601×3601 int16 array from the binary file
- **AND** cache the parsed tile in memory for subsequent queries

### Requirement: Bilinear interpolation
The system SHALL use bilinear interpolation when querying elevation at sub-grid coordinates, producing smooth elevation transitions between DEM grid points.

#### Scenario: Coordinate falls between grid cells
- **WHEN** (lat, lon) does not exactly align with a DEM grid point
- **THEN** the system SHALL compute elevation as the distance-weighted average of the 4 nearest grid cells
- **AND** the result SHALL be within the min-max range of the 4 surrounding cells
