from app.vehicle.interface import VehicleInterface
from app.schemas.telemetry import VehicleTelemetry

class SimulatedVehicle(VehicleInterface):
    def __init__(self):
        self.steering = 0.0
        self.throttle = 0.0
        self.speed = 0.0
        self.brake = False
        self.emergency_stopped = False

    def set_steering(self, value: float) -> None:
       self.steering = max(-1.0, min(1.0, value))

    def set_throttle(self, value: float) -> None:
        if self.brake or self.emergency_stopped:
            self.throttle = 0.0
            return

        self.throttle = max(-1.0, min(1.0, value))

    def set_brake(self, engaged: bool) -> None:
        if self.emergency_stopped:
            self.brake = True
            self.throttle = 0.0
            return
        self.brake = engaged
        if engaged:
            self.throttle = 0.0  

    def emergency_stop(self) -> None:
        self.emergency_stopped = True
        self.speed = 0.0
        self.throttle = 0.0
        self.brake = True
    def reset_emergency_stop(self) -> None:
        self.emergency_stopped = False
        self.brake = False
        self.throttle = 0.0
        self.speed = 0.0    

    def get_state(self) -> VehicleTelemetry:
        return VehicleTelemetry(
            speed=self.speed,
            steering=self.steering, 
            throttle=self.throttle,
            brake=self.brake,
            is_connected=True,
            mode="simulation",
            emergency_stopped=self.emergency_stopped
        )