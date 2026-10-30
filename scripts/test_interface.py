from app.vehicle.interface import VehicleInterface
from app.schemas.telemetry import VehicleTelemetry


def test_vehicle_interface_methods():
    class TestVehicle(VehicleInterface):
        def __init__(self):
            self.steering = 0.0
            self.throttle = 0.0
            self.speed = 0.0
            self.brake = False

        def set_steering(self, value: float) -> None:
            self.steering = value

        def set_throttle(self, value: float) -> None:
            self.throttle = value

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

    vehicle = TestVehicle()
    vehicle.set_steering(0.5)
    vehicle.set_throttle(0.8)

    vehicle.emergency_stop()

    state = vehicle.get_state()

    assert state.speed == 0.0
    assert state.steering == 0.5
    assert state.throttle == 0.0
    assert state.brake is True
    assert state.is_connected is True
    assert state.mode == "simulation"