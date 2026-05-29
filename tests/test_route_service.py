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
