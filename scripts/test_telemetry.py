from app.schemas.telemetry import VehicleTelemetry
from pydantic import ValidationError
import pytest

def test_vehicle_telemetry_model():
    # Create an instance of VehicleTelemetry with valid data
    telemetry_data = {
        "speed": 10.5,
        "steering": 0.5,
        "throttle": 0.8,
        "mode": "simulation"
    }
    telemetry = VehicleTelemetry(**telemetry_data)

    # Assert that the instance is created successfully and the values are correct
    assert telemetry.speed == 10.5
    assert telemetry.steering == 0.5
    assert telemetry.throttle == 0.8
    assert telemetry.brake is False
    assert telemetry.is_connected is False
    assert telemetry.mode == "simulation"

    # Test validation for speed (should raise ValidationError for negative speed)
    with pytest.raises(ValidationError):
        VehicleTelemetry(speed=-1.0, steering=0.0, throttle=0.0, brake=False, is_connected=False, mode="simulation")

    # Test validation for steering (should raise ValidationError for out of range)
    with pytest.raises(ValidationError):
        VehicleTelemetry(speed=0.0, steering=2.0, throttle=0.0, brake=False, is_connected=False, mode="simulation")

    # Test validation for throttle (should raise ValidationError for out of range)
    with pytest.raises(ValidationError):
        VehicleTelemetry(speed=0.0, steering=0.0, throttle=-2.0, brake=False, is_connected=False, mode="simulation")

    with pytest.raises(ValidationError):
        VehicleTelemetry(
        speed=0.0,
        steering=0.0,
        throttle=0.0,
        mode="drone"
    )    