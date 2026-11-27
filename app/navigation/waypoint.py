import math


class Waypoint:
    def __init__(self, x: int | float, y: int | float):
        self.x = self._validate_coord(x, "x")
        self.y = self._validate_coord(y, "y")

    @staticmethod
    def _validate_coord(value: int | float, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number, got {type(value).__name__}")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite, got {value}")
        return float(value)