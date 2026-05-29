from app.services.route_service import parse_gpx, haversine_distance


VALID_GPX = """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/0" version="1.0" creator="行者">
  <name>南昆山 广商</name>
  <trk>
    <trkseg>
      <trkpt lat="23.615807" lon="113.848983">
        <ele>721</ele>
      </trkpt>
      <trkpt lat="23.615805" lon="113.848955">
        <ele>721</ele>
      </trkpt>
      <trkpt lat="23.615801" lon="113.848841">
        <ele>713</ele>
      </trkpt>
    </trkseg>
  </trk>
</gpx>"""


def test_parse_gpx_valid():
    name, points, distance, elevation_gain = parse_gpx(VALID_GPX.encode())
    assert name == "南昆山 广商"
    assert len(points) == 3
    assert points[0]["lat"] == 23.615807
    assert points[0]["lon"] == 113.848983
    assert points[0]["ele"] == 721
    assert distance > 0
    assert elevation_gain == 0


def test_parse_gpx_no_name():
    gpx = VALID_GPX.replace("<name>南昆山 广商</name>", "")
    name, points, distance, _ = parse_gpx(gpx.encode())
    assert name == "未命名路书"
    assert len(points) == 3


def test_parse_gpx_no_track():
    gpx = "<gpx></gpx>"
    name, points, distance, _ = parse_gpx(gpx.encode())
    assert len(points) == 0
    assert distance == 0


def test_parse_gpx_elevation_gain():
    gpx = """<?xml version="1.0"?>
    <gpx><trk><trkseg>
      <trkpt lat="23.0" lon="113.0"><ele>100</ele></trkpt>
      <trkpt lat="23.001" lon="113.001"><ele>120</ele></trkpt>
      <trkpt lat="23.002" lon="113.002"><ele>110</ele></trkpt>
    </trkseg></trk></gpx>"""
    _, _, _, gain = parse_gpx(gpx.encode())
    assert gain == 20.0


def test_haversine_distance():
    d = haversine_distance(23.0, 113.0, 23.001, 113.001)
    assert 100 < d < 200


def test_parse_gpx_no_ele():
    gpx = """<?xml version="1.0"?>
    <gpx><trk><trkseg>
      <trkpt lat="23.0" lon="113.0"></trkpt>
      <trkpt lat="23.001" lon="113.001"></trkpt>
    </trkseg></trk></gpx>"""
    name, points, distance, gain = parse_gpx(gpx.encode())
    assert points[0]["ele"] == 0
    assert gain == 0


def test_parse_gpx_invalid_xml():
    name, points, distance, gain = parse_gpx(b"not xml at all")
    assert name == ""
    assert len(points) == 0


from unittest.mock import patch, MagicMock
from app.services.route_service import upload_gpx_to_oss, download_gpx_from_oss, delete_gpx_from_oss


@patch("app.services.route_service.oss2")
def test_upload_gpx_to_oss(mock_oss2):
    mock_bucket = MagicMock()
    mock_oss2.Auth.return_value = MagicMock()
    mock_oss2.Bucket.return_value = mock_bucket
    mock_bucket.put_object.return_value = MagicMock()

    url = upload_gpx_to_oss(b"gpx content", "test.gpx", 42)

    assert url.startswith("https://")
    mock_bucket.put_object.assert_called_once()


@patch("app.services.route_service.oss2")
def test_download_gpx_from_oss(mock_oss2):
    mock_bucket = MagicMock()
    mock_oss2.Auth.return_value = MagicMock()
    mock_oss2.Bucket.return_value = mock_bucket
    mock_result = MagicMock()
    mock_result.read.return_value = b"gpx content"
    mock_bucket.get_object.return_value = mock_result

    data = download_gpx_from_oss("https://bucket.oss/routes/42/test.gpx")

    assert data == b"gpx content"


@patch("app.services.route_service.oss2")
def test_delete_gpx_from_oss(mock_oss2):
    mock_bucket = MagicMock()
    mock_oss2.Auth.return_value = MagicMock()
    mock_oss2.Bucket.return_value = mock_bucket

    delete_gpx_from_oss("https://bucket.oss/routes/42/test.gpx")
    mock_bucket.delete_object.assert_called_once_with("routes/42/test.gpx")


@patch("app.services.route_service.oss2")
def test_delete_gpx_from_oss_invalid_url(mock_oss2):
    """无效 URL 不抛异常"""
    delete_gpx_from_oss("not-a-valid-oss-url")
