from pydantic import ValidationError
from app.schemas.commands import VehicleCommand


def test_vehicle_command_schema():
    valid_data = {
        "steering": 0.5,
        "throttle": 0.8,
        "brake": True
    }

    command = VehicleCommand(**valid_data)

    assert command.steering == 0.5
    assert command.throttle == 0.8
    assert command.brake is True

    invalid_steering_data = {
        "steering": 1.5,
        "throttle": 0.5,
        "brake": False
    }

    try:
        VehicleCommand(**invalid_steering_data)
        assert False, "Expected ValidationError for invalid steering"
    except ValidationError as e:
        assert "steering" in str(e)

    invalid_throttle_data = {
        "steering": 0.0,
        "throttle": -1.5,
        "brake": False
    }

    try:
        VehicleCommand(**invalid_throttle_data)
        assert False, "Expected ValidationError for invalid throttle"
    except ValidationError as e:
        assert "throttle" in str(e)

    reverse_data = {
        "steering": 0.0,
        "throttle": -1.0
    }

    reverse_command = VehicleCommand(**reverse_data)

    assert reverse_command.throttle == -1.0
    assert reverse_command.brake is False

    command = VehicleCommand(
        steering=0.0,
        throttle=0.5
    )

    assert command.brake is False