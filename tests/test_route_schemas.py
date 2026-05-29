from datetime import datetime

from app.api.v1.schemas import RouteImportResponse, RouteListItem, RouteDetailResponse, RouteExportPlanRequest


def test_route_import_response():
    resp = RouteImportResponse(
        id=1,
        name="南昆山",
        distance=50000.0,
        elevation_gain=800.0,
        track_points=2000,
    )
    assert resp.id == 1
    assert resp.name == "南昆山"
    assert resp.distance == 50000.0


def test_route_list_item():
    item = RouteListItem(
        id=1,
        name="南昆山",
        distance=50000.0,
        source="import",
        created_at=datetime(2026, 5, 29, 12, 0, 0),
    )
    assert item.id == 1
    assert item.source == "import"


def test_route_detail_response():
    detail = RouteDetailResponse(
        id=1,
        name="南昆山",
        distance=50000.0,
        elevation_gain=800.0,
        track_points=2000,
        source="import",
        created_at=datetime(2026, 5, 29, 12, 0, 0),
        track_data=[{"lat": 23.615, "lon": 113.848, "ele": 721}],
    )
    assert len(detail.track_data) == 1
    assert detail.track_data[0].lat == 23.615


def test_route_export_plan_request():
    req = RouteExportPlanRequest(
        name="我的路线",
        coordinates=[{"lat": 23.615, "lon": 113.848}, {"lat": 23.616, "lon": 113.849}],
    )
    assert len(req.coordinates) == 2
