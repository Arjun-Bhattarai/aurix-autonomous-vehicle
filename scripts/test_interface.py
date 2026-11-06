from app.vehicle.interface import VehicleInterface
from app.schemas.telemetry import VehicleTelemetry
import pytest

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
        def set_brake(self, engaged: bool) -> None:
            self.brake = engaged

        def reset_emergency_stop(self) -> None:
            self.brake = False
            self.throttle = 0.0
            self.speed = 0.0   

        def reset_communication_timeout(self) -> None:
            pass
        def get_last_command_time(self) -> float:
            return 0.0
        def update(self) -> None:
            pass     

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
    assert vehicle.brake is True

    vehicle.reset_emergency_stop()

    state = vehicle.get_state()

    assert state.speed == 0.0
    assert state.steering == 0.5
    assert state.throttle == 0.0
    assert state.brake is False
    assert state.is_connected is True
    assert state.mode == "simulation"
    assert vehicle.brake is False


def test_incomplete_vehicle_cannot_be_instantiated():
    class IncompleteVehicle(VehicleInterface):
        def set_steering(self, value: float) -> None:
            pass

        def set_throttle(self, value: float) -> None:
            pass

        def emergency_stop(self) -> None:
            pass

        def get_state(self) -> VehicleTelemetry:
            return VehicleTelemetry(
                speed=0.0,
                steering=0.0,
                throttle=0.0,
                brake=False,
                is_connected=True,
                mode="simulation"
            )
        def set_brake(self, engaged: bool) -> None:
            pass

    with pytest.raises(TypeError, match="abstract"):
        IncompleteVehicle()
    