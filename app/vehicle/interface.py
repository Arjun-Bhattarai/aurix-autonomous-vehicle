
from abc import ABC, abstractmethod

from app.schemas.telemetry import VehicleTelemetry


class VehicleInterface(ABC):

    @abstractmethod
    def set_steering(self, value: float) -> None:
        """Set steering between -1.0 (left) and 1.0 (right)."""
        pass

    @abstractmethod
    def set_throttle(self, value: float) -> None:
        """Set throttle between -1.0 (reverse) and 1.0 (forward)."""
        pass

    @abstractmethod
    def emergency_stop(self) -> None:
        """Immediately stop the vehicle."""
        pass

    @abstractmethod
    def get_state(self) -> VehicleTelemetry:
        """Return the current vehicle telemetry."""
        pass
