import math

from app.navigation.waypoint import Waypoint


class PathPlanner:
    def __init__(self, waypoints: list[Waypoint]):
        if not isinstance(waypoints, (list, tuple)):
            raise TypeError(
                f"waypoints must be a list or tuple, got {type(waypoints).__name__}"
            )
        for index, wp in enumerate(waypoints):
            if not isinstance(wp, Waypoint):
                raise TypeError(
                    f"waypoints[{index}] must be a Waypoint, got {type(wp).__name__}"
                )
        self.waypoints: list[Waypoint] = list(waypoints)

    def calculate_direction(self, index: int) -> float | None:
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError(f"index must be an int, got {type(index).__name__}")
        if index < 0 or index >= len(self.waypoints) - 1:
            raise IndexError("Index out of range for direction calculation.")

        wp1 = self.waypoints[index]
        wp2 = self.waypoints[index + 1]
        delta_x = wp2.x - wp1.x
        delta_y = wp2.y - wp1.y

        if delta_x == 0.0 and delta_y == 0.0:
            return None

        return math.atan2(delta_y, delta_x)

    def calculate_direction(self, index: int) -> float:
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError(f"index must be an int, got {type(index).__name__}")
        if index < 0 or index >= len(self.waypoints) - 1:
            raise IndexError("Index out of range for direction calculation.")

        wp1 = self.waypoints[index]
        wp2 = self.waypoints[index + 1]
        return math.atan2(wp2.y - wp1.y, wp2.x - wp1.x)