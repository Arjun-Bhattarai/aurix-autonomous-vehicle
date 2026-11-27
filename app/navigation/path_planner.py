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

    def calculate_path_length(self) -> float:
        total_length = 0.0
        for i in range(len(self.waypoints) - 1):
            wp1 = self.waypoints[i]
            wp2 = self.waypoints[i + 1]
            total_length += math.hypot(wp2.x - wp1.x, wp2.y - wp1.y)
        return float(total_length)