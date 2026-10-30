from app.vehicle.interface import VehicleInterface
from app.schemas.telemetry import VehicleTelemetry

class SimulatedVehicle(VehicleInterface):
    def __init__(self):
        self.steering = 0.0
        self.throttle = 0.0
        self.speed = 0.0
        self.brake = False

    def set_steering(self, value: float) -> None:
       self.steering = max(-1.0, min(1.0, value))

    def set_throttle(self, value: float) -> None:
        self.throttle =max(-1.0, min(1.0, value))

    def emergency_stop(self) -> None:
        self.speed = 0.0
        self.throttle = 0.0
        self.brake = True

    def get_state(self) -> VehicleTelemetry:
        return VehicleTelemetry(
            speed=self.speed,
            steering=self.steering, 
            throttle=self.throttle,
            brake=self.brake,
            is_connected=True,
            mode="simulation"
        )