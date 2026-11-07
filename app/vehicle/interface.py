
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
    @abstractmethod
    def get_last_command_time(self) -> float:
        """Return the time of the last command."""
        pass
    @abstractmethod
    def update(self) -> None:
        """Update the vehicle's state."""
        pass
    @abstractmethod
    def set_brake(self, engaged: bool) -> None:
        """Set the brake state."""
        pass
    @abstractmethod
    def reset_emergency_stop(self) -> None:
        """Reset the emergency stop state."""
        pass
    @abstractmethod
    def reset_communication_timeout(self) -> None:
        """Reset the communication timeout state."""
        pass

    @abstractmethod
    def receive_heartbeat(self) -> None:
        """Simulate receiving a heartbeat from the controller."""
        pass
