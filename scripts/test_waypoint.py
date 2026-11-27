import pytest
from app.navigation.waypoint import Waypoint

def test_waypoint_initialization():
    wp = Waypoint(10, 20)
    assert isinstance(wp, Waypoint)
    assert wp.x == 10.0
    assert wp.y == 20.0
    assert isinstance(wp.x, float)
    assert isinstance(wp.y, float)

    wp = Waypoint(10.5, 20.5)
    assert isinstance(wp, Waypoint)
    assert wp.x == 10.5
    assert wp.y == 20.5
    assert isinstance(wp.x, float)
    assert isinstance(wp.y, float)

    wp = Waypoint(-5, -15)
    assert isinstance(wp, Waypoint)
    assert wp.x == -5.0
    assert wp.y == -15.0
    assert isinstance(wp.x, float)
    assert isinstance(wp.y, float)

def test_waypoint_rejects_string_coordinate():
    with pytest.raises(TypeError):
        Waypoint("10", 20)  # type: ignore[arg-type]


def test_waypoint_rejects_bool_coordinate():
    with pytest.raises(TypeError):
        Waypoint(True, 20)  # type: ignore[arg-type]


def test_waypoint_rejects_nan_coordinate():
    with pytest.raises(ValueError):
        Waypoint(float("nan"), 0.0)


def test_waypoint_rejects_inf_coordinate():
    with pytest.raises(ValueError):
        Waypoint(0.0, float("inf"))