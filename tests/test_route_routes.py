import sys
from unittest.mock import MagicMock, AsyncMock, patch

# Mock heavy dependencies before importing main
sys.modules["langgraph"] = MagicMock()
sys.modules["langgraph.checkpoint"] = MagicMock()
sys.modules["langgraph.checkpoint.sqlite"] = MagicMock()
sys.modules["langgraph.checkpoint.sqlite.aio"] = MagicMock()
sys.modules["app.agents"] = MagicMock()
sys.modules["app.db"] = MagicMock()
sys.modules["app.redis_client"] = MagicMock()

import os
# Ensure required env vars are set to avoid main.py startup error
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LLM_MODEL", "test-model")
os.environ.setdefault("BAIDU_MAPS_API_KEY", "test-baidu-key")
os.environ.setdefault("BAIDU_MAPS_JS_AK", "test-baidu-ak")

from main import app
import pytest
from httpx import AsyncClient, ASGITransport


def _make_mock_session():
    """Create a mock MySQL session with async context manager support."""
    mock_session = AsyncMock()
    mock_ctx = MagicMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
    mock_ctx.__aexit__ = AsyncMock(return_value=None)
    return mock_session, mock_ctx


@pytest.fixture
def override_deps():
    from app.auth.dependencies import get_current_user
    app.dependency_overrides[get_current_user] = lambda: MagicMock(id=42)
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_routes_empty(override_deps):
    from app.api.v1 import route_routes as rr
    with patch.object(rr, "db_mysql") as mock_db:
        mock_session, mock_ctx = _make_mock_session()
        mock_db.async_session_factory = MagicMock(return_value=mock_ctx)
        result_mock = MagicMock()
        result_mock.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = result_mock

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get(
                "/api/routes",
                headers={"Authorization": "Bearer test-token"},
            )
            assert resp.status_code == 200
            data = resp.json()
            assert data["routes"] == []


@pytest.mark.asyncio
async def test_import_gpx_success(override_deps):
    gpx_content = """<?xml version="1.0"?>
    <gpx><name>测试</name><trk><trkseg>
      <trkpt lat="23.0" lon="113.0"><ele>100</ele></trkpt>
    </trkseg></trk></gpx>""".encode("utf-8")

    from app.api.v1 import route_routes as rr
    with patch.object(rr, "db_mysql") as mock_db, \
         patch.object(rr, "upload_gpx_to_oss") as mock_upload, \
         patch.object(rr, "parse_gpx") as mock_parse:

        mock_session, mock_ctx = _make_mock_session()
        mock_db.async_session_factory = MagicMock(return_value=mock_ctx)

        # Sync methods on AsyncSession (not awaited)
        mock_session.add = MagicMock()

        async def mock_refresh(obj):
            obj.id = 1

        mock_session.refresh = mock_refresh

        mock_upload.return_value = "https://bucket.oss/routes/42/test.gpx"
        mock_parse.return_value = ("测试", [{"lat": 23.0, "lon": 113.0, "ele": 100}], 0.0, 0.0)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                "/api/routes/import",
                files={"file": ("test.gpx", gpx_content, "application/gpx+xml")},
                headers={"Authorization": "Bearer test-token"},
            )
            assert resp.status_code == 201
            data = resp.json()
            assert data["name"] == "测试"


@pytest.mark.asyncio
async def test_import_gpx_wrong_extension(override_deps):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/routes/import",
            files={"file": ("test.txt", b"not gpx", "text/plain")},
            headers={"Authorization": "Bearer test-token"},
        )
        assert resp.status_code == 400


@pytest.mark.asyncio
async def test_export_plan(override_deps):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/routes/export-plan",
            json={
                "name": "我的路线",
                "coordinates": [
                    {"lat": 23.615, "lon": 113.848},
                    {"lat": 23.616, "lon": 113.849, "ele": 100},
                ],
            },
            headers={"Authorization": "Bearer test-token"},
        )
        assert resp.status_code == 200
        assert "attachment" in resp.headers.get("content-disposition", "")
