import pytest
import math

from app.navigation.path_planner import PathPlanner
from app.navigation.waypoint import Waypoint


def test_path_planner_initialization():
    wp1 = Waypoint(0, 0)
    wp2 = Waypoint(3, 4)
    planner = PathPlanner([wp1, wp2])

    assert isinstance(planner, PathPlanner)
    assert len(planner.waypoints) == 2
    assert planner.waypoints[0] == wp1
    assert planner.waypoints[1] == wp2


def test_path_planner_empty_initialization_and_length():
    planner = PathPlanner([])

    assert isinstance(planner, PathPlanner)
    assert len(planner.waypoints) == 0
    assert planner.calculate_path_length() == 0.0

def test_path_planner_calculate_path_length():
    planner = PathPlanner([Waypoint(0, 0), Waypoint(3, 4), Waypoint(3, 8)])

    assert planner.calculate_path_length() == pytest.approx(9.0)


def test_path_planner_rejects_non_list_input():
    with pytest.raises(TypeError):
        PathPlanner("not a list")  


def test_path_planner_rejects_non_waypoint_elements():
    with pytest.raises(TypeError):
        PathPlanner([Waypoint(0, 0), "not a waypoint"])

def test_calculate_direction_segments():
    planner = PathPlanner([Waypoint(0, 0), Waypoint(3, 4), Waypoint(3, 8)])

    assert planner.calculate_direction(0) == pytest.approx(math.atan2(4, 3))
    assert planner.calculate_direction(1) == pytest.approx(math.pi / 2)


def test_calculate_direction_out_of_range_index():
    planner = PathPlanner([Waypoint(0, 0), Waypoint(3, 4), Waypoint(3, 8)])

    with pytest.raises(IndexError):
        planner.calculate_direction(2)


def test_calculate_direction_rejects_float_index():
    planner = PathPlanner([Waypoint(0, 0), Waypoint(3, 4), Waypoint(3, 8)])

    with pytest.raises(TypeError):
        planner.calculate_direction(1.5)  # type: ignore[arg-type]


def test_calculate_direction_rejects_bool_index():
    planner = PathPlanner([Waypoint(0, 0), Waypoint(3, 4), Waypoint(3, 8)])

    with pytest.raises(TypeError):
        planner.calculate_direction(True)  # type: ignore[arg-type]
