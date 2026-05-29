from datetime import datetime
from app.models import Route


def test_route_model_fields():
    """验证 Route 模型字段定义正确"""
    route = Route(
        id=1,
        user_id=42,
        name="南昆山 广商",
        description="一条好路线",
        gpx_oss_url="https://bucket.oss/routes/42/123_abc.gpx",
        distance=52300.5,
        elevation_gain=1200.3,
        track_points=3500,
        source="import",
        created_at=datetime(2026, 5, 29, 12, 0, 0),
        updated_at=datetime(2026, 5, 29, 12, 0, 0),
    )
    assert route.name == "南昆山 广商"
    assert route.distance == 52300.5
    assert route.elevation_gain == 1200.3
    assert route.track_points == 3500
    assert route.source == "import"


def test_route_source_values():
    """验证 source 字段接受 import 和 agent"""
    route_import = Route(user_id=1, name="test", gpx_oss_url="", distance=0, elevation_gain=0, track_points=0, source="import")
    assert route_import.source == "import"

    route_agent = Route(user_id=1, name="test", gpx_oss_url="", distance=0, elevation_gain=0, track_points=0, source="agent")
    assert route_agent.source == "agent"
