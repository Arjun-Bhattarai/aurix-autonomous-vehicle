import math
import time
from app.schemas.telemetry import VehicleTelemetry
from app.vehicle.interface import VehicleInterface


class SimulatedVehicle(VehicleInterface):
    def __init__(self, command_timeout: float = 2.0):
        if isinstance(command_timeout, bool) or not isinstance(command_timeout, (int, float)):
            raise TypeError(
                f"command_timeout must be a number, got {type(command_timeout).__name__}"
            )
        if not math.isfinite(command_timeout) or command_timeout <= 0:
            raise ValueError(
                f"command_timeout must be a finite number greater than 0 seconds, got {command_timeout}"
            )

        self.steering: float = 0.0
        self.throttle: float = 0.0
        self.speed: float = 0.0
        self.heading: float = 0.0
        self.x: float = 0.0
        self.y: float = 0.0
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

        # Steering and vehicle geometry
        self.wheelbase: float = 0.25  # meters
        self.max_steering_angle: float = 30.0  # degrees

    def _heartbeat(self) -> None:
        """Strictly update the last command timestamp."""
        self.last_command_time = time.monotonic()

    def set_steering(self, value: float) -> None:
        self.steering = max(-1.0, min(1.0, value))

    def set_throttle(self, value: float) -> None:
        # Block throttle if brake, emergency stop, or communication timeout is active
        if self.brake or self.emergency_stopped or self.communication_timed_out:
            self.throttle = 0.0
            return
        self.throttle = max(-1.0, min(1.0, value))

    def set_brake(self, engaged: bool) -> None:
        """Guard brake release against active emergency stop or active timeout."""
        if not engaged and (self.emergency_stopped or self.communication_timed_out):
            return

        self.brake = engaged
        if engaged:
            self.throttle = 0.0

    def emergency_stop(self) -> None:
        self.emergency_stopped = True
        self.throttle = 0.0
        self.brake = True
        self.speed = 0.0

    def reset_emergency_stop(self) -> None:
        self.emergency_stopped = False
        self.brake = False  # Keep brake engaged until explicitly released
        self.throttle = 0.0
        self.speed = 0.0

    def reset_communication_timeout(self) -> None:
        time_since_last_command = time.monotonic() - self.last_command_time
        if time_since_last_command > self.command_timeout:
            raise RuntimeError(
                "Cannot reset communication timeout: "
                "No fresh controller command received."
            )
        self.communication_timed_out = False

    def get_state(self) -> VehicleTelemetry:
        is_connected = (time.monotonic() - self.last_command_time) <= self.command_timeout
        return VehicleTelemetry(
            speed=self.speed,
            steering=self.steering,
            throttle=self.throttle,
            brake=self.brake,
            is_connected=is_connected,
            mode="simulation",
            emergency_stopped=self.emergency_stopped,
            communication_timed_out=self.communication_timed_out,
            heading=self.heading,
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

        # Kinematic bicycle model: positive steering = right (clockwise = negative yaw rate)
        steering_angle = math.radians(self.steering * self.max_steering_angle)
        yaw_rate = -(self.speed / self.wheelbase) * math.tan(steering_angle)

        start_heading = self.heading
        mid_heading = start_heading + 0.5 * yaw_rate * delta_time
        end_heading = start_heading + yaw_rate * delta_time

        self.x += self.speed * math.cos(mid_heading) * delta_time
        self.y += self.speed * math.sin(mid_heading) * delta_time

        self.heading = ((end_heading + math.pi) % (2 * math.pi)) - math.pi

    

        if self.brake or self.communication_timed_out:
            decel = self.braking_rate * delta_time
            if self.speed > 0.0:
                self.speed = max(0.0, self.speed - decel)
            elif self.speed < 0.0:
                self.speed = min(0.0, self.speed + decel)
        elif self.throttle != 0:
            self.speed += self.throttle * self.acceleration_rate * delta_time
        else:
            drag = self.coasting_drag * delta_time
            if self.speed > 0.0:
                self.speed = max(0.0, self.speed - drag)
            elif self.speed < 0.0:
                self.speed = min(0.0, self.speed + drag)

        self.speed = max(-self.max_speed, min(self.max_speed, self.speed))

    def get_last_command_time(self) -> float:
        return self.last_command_time

    def receive_heartbeat(self) -> None:
        """Simulate receiving an isolated heartbeat from the controller."""
        self._heartbeat()