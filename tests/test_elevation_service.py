from unittest.mock import patch, MagicMock

from app.services.elevation_service import (
    haversine_distance,
    sample_points,
    calculate_elevation_stats,
    lookup_elevations,
    extract_coordinates,
)


def test_haversine_distance():
    d = haversine_distance(23.0, 113.0, 23.001, 113.001)
    assert 100 < d < 200


def test_haversine_distance_same_point():
    d = haversine_distance(23.0, 113.0, 23.0, 113.0)
    assert d == 0


def test_sample_points_empty():
    assert sample_points([]) == []


def test_sample_points_single():
    assert sample_points([{"lat": 23.0, "lon": 113.0}]) == [{"lat": 23.0, "lon": 113.0}]


def test_sample_points_two():
    points = [{"lat": 23.0, "lon": 113.0}, {"lat": 23.1, "lon": 113.1}]
    assert len(sample_points(points)) == 2


def test_sample_points_dense():
    """密集点应被采样减少"""
    points = []
    for i in range(100):
        points.append({"lat": 23.0 + i * 0.0001, "lon": 113.0 + i * 0.0001})
    sampled = sample_points(points, interval_m=500.0)
    assert len(sampled) < len(points)
    assert sampled[0] == points[0]
    assert sampled[-1] == points[-1]


def test_calculate_elevation_stats_gain():
    points = [
        {"lat": 23.0, "lon": 113.0, "ele": 100},
        {"lat": 23.001, "lon": 113.001, "ele": 120},
        {"lat": 23.002, "lon": 113.002, "ele": 110},
    ]
    stats = calculate_elevation_stats(points)
    assert stats["elevation_gain"] == 20.0
    assert stats["elevation_loss"] == 10.0
    assert stats["max_elevation"] == 120
    assert stats["min_elevation"] == 100


def test_calculate_elevation_stats_flat():
    points = [
        {"lat": 23.0, "lon": 113.0, "ele": 50},
        {"lat": 23.001, "lon": 113.001, "ele": 50},
    ]
    stats = calculate_elevation_stats(points)
    assert stats["elevation_gain"] == 0
    assert stats["elevation_loss"] == 0


def test_calculate_elevation_stats_empty():
    stats = calculate_elevation_stats([])
    assert stats["elevation_gain"] == 0
    assert stats["max_elevation"] == 0


@patch("app.services.elevation_service.urllib.request.urlopen")
def test_lookup_elevations(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = (
        b'{"results":['
        b'{"latitude":23.0,"longitude":113.0,"elevation":100},'
        b'{"latitude":23.001,"longitude":113.001,"elevation":120}'
        b']}'
    )
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    points = [
        {"lat": 23.0, "lon": 113.0},
        {"lat": 23.001, "lon": 113.001},
    ]
    result = lookup_elevations(points)
    assert len(result) == 2
    assert result[0] == {"lat": 23.0, "lon": 113.0, "ele": 100}
    assert result[1] == {"lat": 23.001, "lon": 113.001, "ele": 120}


def test_extract_coordinates_from_path():
    text = '{"routes":[{"steps":[{"path":"116.4,39.9;116.41,39.91;116.42,39.92"}]}]}'
    points = extract_coordinates(text)
    assert len(points) == 3
    assert points[0] == {"lat": 39.9, "lon": 116.4}


def test_extract_coordinates_from_bracketed_pairs():
    text = "路线经过 (39.9042, 116.4074) 和 (39.9142, 116.4174)"
    points = extract_coordinates(text)
    assert len(points) == 2
    assert points[0] == {"lat": 39.9042, "lon": 116.4074}


def test_extract_coordinates_no_coords():
    points = extract_coordinates("没有坐标的文本")
    assert points == []


def test_extract_coordinates_multiple_paths():
    text = '''
    {"steps": [
      {"path": "113.0,23.0;113.001,23.001"},
      {"path": "113.002,23.002"}
    ]}
    '''
    points = extract_coordinates(text)
    assert len(points) == 3
