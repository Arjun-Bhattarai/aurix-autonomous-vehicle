import time
from app.vehicle.interface import VehicleInterface
from app.schemas.telemetry import VehicleTelemetry


class SimulatedVehicle(VehicleInterface):
    def __init__(self, command_timeout: float = 2.0):
        self.steering: float = 0.0
        self.throttle: float = 0.0
        self.speed: float = 0.0
        self.brake: bool = False
        self.emergency_stopped: bool = False

        # Communication watchdog
        self.command_timeout: float = command_timeout
        self.communication_timed_out: bool = False

        now = time.monotonic()
        self.last_update_time: float = now
        self.last_command_time: float = now

        # Vehicle physics constants
        self.max_speed: float = 30.0  # m/s
        self.acceleration_rate: float = 5.0
        self.braking_rate: float = 8.0
        self.coasting_drag: float = 1.0

    def _heartbeat(self) -> None:
        """Step 1: Strictly update the last command timestamp."""
        self.last_command_time = time.monotonic()

    def set_steering(self, value: float) -> None:
        self._heartbeat()
        self.steering = max(-1.0, min(1.0, value))

    def set_throttle(self, value: float) -> None:
        self._heartbeat()
        # Block throttle if brake, emergency stop, or communication timeout is active
        if self.brake or self.emergency_stopped or self.communication_timed_out:
            self.throttle = 0.0
            return
        self.throttle = max(-1.0, min(1.0, value))

    def set_brake(self, engaged: bool) -> None:
        """Step 2: Guard brake release against active emergency stop or active timeout."""
        self._heartbeat()

        if not engaged and (self.emergency_stopped or self.communication_timed_out):
            return

        self.brake = engaged
        if engaged:
            self.throttle = 0.0

    def emergency_stop(self) -> None:
        self._heartbeat()
        self.emergency_stopped = True
        self.throttle = 0.0
        self.brake = True
        self.speed = 0.0

    def reset_emergency_stop(self) -> None:
        self._heartbeat()
        self.emergency_stopped = False
        self.brake = False  # Keep brake engaged until explicitly released
        self.throttle = 0.0
        self.speed = 0.0

    def reset_communication_timeout(self) -> None:
        """Step 3: Reset the timeout flag without altering brake or throttle state."""
        self._heartbeat()
        self.communication_timed_out = False

    def get_state(self) -> VehicleTelemetry:
        return VehicleTelemetry(
            speed=self.speed,
            steering=self.steering,
            throttle=self.throttle,
            brake=self.brake,
            is_connected=not self.communication_timed_out,
            mode="simulation",
            emergency_stopped=self.emergency_stopped,
            communication_timed_out=self.communication_timed_out,
        )

    def update(self) -> None:
        current_time = time.monotonic()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time

        # Watchdog trigger
        if current_time - self.last_command_time > self.command_timeout:
            self.communication_timed_out = True
            self.throttle = 0.0
            self.brake = True
            self.steering = 0.0

        if self.emergency_stopped:
            self.speed = 0.0
            return

        # Apply physics based on current vehicle state
        if self.brake or self.communication_timed_out:
            self.speed = max(0.0, self.speed - self.braking_rate * delta_time)
        elif self.throttle > 0:
            self.speed += self.throttle * self.acceleration_rate * delta_time
            self.speed = min(self.speed, self.max_speed)
        else:
            self.speed = max(0.0, self.speed - self.coasting_drag * delta_time)

    def get_last_command_time(self) -> float:
        return self.last_command_time