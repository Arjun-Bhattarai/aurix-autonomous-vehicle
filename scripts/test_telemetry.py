import pytest
from pydantic import ValidationError

from app.schemas.telemetry import VehicleTelemetry


def test_vehicle_telemetry_model():
    telemetry_data = {
        "speed": 10.5,
        "steering": 0.5,
        "throttle": 0.8,
        "mode": "simulation",
    }
    telemetry = VehicleTelemetry(**telemetry_data)

    assert telemetry.speed == 10.5
    assert telemetry.steering == 0.5
    assert telemetry.throttle == 0.8
    assert telemetry.brake is False
    assert telemetry.is_connected is False
    assert telemetry.mode == "simulation"

    # Negative speed within bounds is valid for reverse motion
    reverse_telemetry = VehicleTelemetry(
        speed=-1.0,
        steering=0.0,
        throttle=-0.5,
        brake=False,
        is_connected=False,
        mode="simulation",
    )
    assert reverse_telemetry.speed == -1.0

    # Test validation for speed out of range
    with pytest.raises(ValidationError):
        VehicleTelemetry(
            speed=-101.0,
            steering=0.0,
            throttle=0.0,
            brake=False,
            is_connected=False,
            mode="simulation",
        )

    # Test validation for steering out of range
    with pytest.raises(ValidationError):
        VehicleTelemetry(
            speed=0.0,
            steering=2.0,
            throttle=0.0,
            brake=False,
            is_connected=False,
            mode="simulation",
        )

    # Test validation for throttle out of range
    with pytest.raises(ValidationError):
        VehicleTelemetry(
            speed=0.0,
            steering=0.0,
            throttle=-2.0,
            brake=False,
            is_connected=False,
            mode="simulation",
        )

    # Test validation for invalid mode literal
    with pytest.raises(ValidationError):
        VehicleTelemetry(
            speed=0.0,
            steering=0.0,
            throttle=0.0,
            mode="drone",
        )