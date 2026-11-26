import math
import time
import pytest
from pytest import raises
from app.vehicle.simulator import SimulatedVehicle


def test_simulated_vehicle():
    vehicle = SimulatedVehicle()

    # Test initial state
    state = vehicle.get_state()
    assert state.speed == 0.0
    assert state.steering == 0.0
    assert state.throttle == 0.0
    assert state.brake is False
    assert state.is_connected is True
    assert state.mode == "simulation"

    # Test setting steering and throttle
    vehicle.set_steering(0.5)
    vehicle.set_throttle(0.8)
    state = vehicle.get_state()
    assert state.steering == 0.5
    assert state.throttle == 0.8

    # Test emergency stop
    vehicle.emergency_stop()
    assert vehicle.emergency_stopped is True
    state = vehicle.get_state()
    assert state.speed == 0.0
    assert state.throttle == 0.0
    assert state.brake is True


def test_control_values_are_clamped():
    vehicle = SimulatedVehicle()

    vehicle.set_steering(2.0)
    vehicle.set_throttle(-2.0)

    state = vehicle.get_state()

    assert state.steering == 1.0
    assert state.throttle == -1.0


def test_emergency_stop_latches_throttle():
    vehicle = SimulatedVehicle()

    vehicle.emergency_stop()
    vehicle.set_throttle(0.8)

    state = vehicle.get_state()

    assert state.throttle == 0.0
    assert state.brake is True
    assert vehicle.emergency_stopped is True


def test_emergency_brake_cannot_be_released():
    vehicle = SimulatedVehicle()

    vehicle.emergency_stop()
    vehicle.set_brake(False)

    state = vehicle.get_state()

    assert state.brake is True
    assert state.throttle == 0.0
    assert vehicle.emergency_stopped is True


def test_reset_emergency_stop():
    vehicle = SimulatedVehicle()

    vehicle.emergency_stop()
    assert vehicle.emergency_stopped is True
    assert vehicle.brake is True

    vehicle.reset_emergency_stop()

    state = vehicle.get_state()

    assert vehicle.emergency_stopped is False
    assert state.brake is False  # Brake is released on reset
    assert state.speed == 0.0
    assert state.throttle == 0.0

    vehicle.set_throttle(0.5)
    updated_state = vehicle.get_state()
    assert updated_state.throttle == 0.5  # Throttle now succeeds


def test_reset_communication_timeout():
    vehicle = SimulatedVehicle()

    # Simulate communication timeout state
    vehicle.communication_timed_out = True
    vehicle.brake = True

    # Throttle should be blocked during timeout
    vehicle.set_throttle(0.5)
    state = vehicle.get_state()
    assert state.throttle == 0.0
    assert state.is_connected is True  # Heartbeat is still fresh, so vehicle is considered connected
    assert state.communication_timed_out is True

    # 1. Reset communication timeout flag
    vehicle.reset_communication_timeout()

    state_after_reset = vehicle.get_state()
    assert state_after_reset.communication_timed_out is False
    assert state_after_reset.is_connected is True
    # Resetting timeout must NOT automatically release brake
    assert state_after_reset.brake is True

    # 2. Throttle must still be blocked because brake is still engaged
    vehicle.set_throttle(0.5)
    assert vehicle.get_state().throttle == 0.0

    # 3. Explicitly release brake
    vehicle.set_brake(False)
    assert vehicle.get_state().brake is False

    # 4. Fresh throttle command should now succeed
    vehicle.set_throttle(0.5)
    updated_state = vehicle.get_state()
    assert updated_state.throttle == 0.5


def test_communication_watchdog_detects_timeout():
    vehicle = SimulatedVehicle(command_timeout=0.1)
    # Make last_command_time stale (0.2s > 0.1s timeout)
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()

    state = vehicle.get_state()
    assert state.brake is True
    assert state.throttle == 0.0
    assert state.communication_timed_out is True
    assert state.is_connected is False

    # Send a fresh heartbeat to satisfy the recovery precondition
    vehicle.receive_heartbeat()

    # Now reset should succeed
    vehicle.reset_communication_timeout()

    state_after_reset = vehicle.get_state()
    assert state_after_reset.communication_timed_out is False
    assert state_after_reset.is_connected is True


def test_receive_heartbeat_updates_timestamp():
    vehicle = SimulatedVehicle()
    initial_time = vehicle.last_command_time

    time.sleep(0.01)  # Ensure some time has passed
    vehicle.receive_heartbeat()

    assert vehicle.last_command_time > initial_time


def test_receive_heartbeat_does_not_clear_timeout():
    vehicle = SimulatedVehicle(command_timeout=0.1)
    # Make last_command_time stale to trigger timeout
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()
    assert vehicle.brake is True
    assert vehicle.communication_timed_out is True

    # Receive heartbeat, but do not send a fresh command
    vehicle.receive_heartbeat()
    assert vehicle.brake is True

    # The timeout state should still be active
    assert vehicle.communication_timed_out is True


def test_receive_heartbeat_does_not_release_brake():
    vehicle = SimulatedVehicle(command_timeout=0.1)
    # Make last_command_time stale to trigger timeout
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()
    assert vehicle.brake is True
    assert vehicle.communication_timed_out is True

    # Receive heartbeat, but do not send a fresh command
    vehicle.receive_heartbeat()
    assert vehicle.brake is True

    # The brake should still be engaged
    assert vehicle.get_state().brake is True


def test_connection_status_before_watchdog_update():
    vehicle = SimulatedVehicle(command_timeout=0.1)
    assert vehicle.get_state().is_connected is True

    vehicle.last_command_time = time.monotonic() - 0.2

    assert vehicle.get_state().is_connected is False
    assert vehicle.get_state().communication_timed_out is False

    vehicle.update()

    assert vehicle.get_state().is_connected is False
    assert vehicle.get_state().communication_timed_out is True


def test_heartbeat_requires_explicit_timeout_reset():
    vehicle = SimulatedVehicle(command_timeout=0.1)
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()
    assert vehicle.get_state().communication_timed_out is True

    vehicle.receive_heartbeat()
    assert vehicle.get_state().communication_timed_out is True
    assert vehicle.get_state().is_connected is True
    assert vehicle.get_state().brake is True

    vehicle.reset_communication_timeout()
    assert vehicle.get_state().communication_timed_out is False
    assert vehicle.get_state().is_connected is True
    assert vehicle.get_state().brake is True


def test_reset_communication_timeout_requires_fresh_heartbeat():
    vehicle = SimulatedVehicle(command_timeout=0.1)
    vehicle.last_command_time = time.monotonic() - 0.2
    vehicle.update()
    assert vehicle.get_state().communication_timed_out is True
    assert vehicle.get_state().is_connected is False
    assert vehicle.get_state().brake is True

    with raises(RuntimeError, match="Cannot reset communication timeout: No fresh controller command received."):
        vehicle.reset_communication_timeout()
    assert vehicle.get_state().communication_timed_out is True


def test_command_timeout_positive_accepted():
    vehicle = SimulatedVehicle(command_timeout=5.0)
    assert vehicle.command_timeout == 5.0


def test_command_timeout_zero_raises_value_error():
    with pytest.raises(ValueError):
        SimulatedVehicle(command_timeout=0)


def test_command_timeout_negative_raises_value_error():
    with pytest.raises(ValueError):
        SimulatedVehicle(command_timeout=-1)


def test_command_timeout_string_raises_type_error():
    with pytest.raises(TypeError):
        SimulatedVehicle(command_timeout="5")


def test_command_timeout_nan_raises_value_error():
    with pytest.raises(ValueError):
        SimulatedVehicle(command_timeout=float("nan"))


def test_command_timeout_pos_inf_raises_value_error():
    with pytest.raises(ValueError):
        SimulatedVehicle(command_timeout=float("inf"))


def test_command_timeout_neg_inf_raises_value_error():
    with pytest.raises(ValueError):
        SimulatedVehicle(command_timeout=float("-inf"))


def test_reverse_acceleration():
    vehicle = SimulatedVehicle()

    # Set throttle to reverse
    vehicle.set_throttle(-0.5)
    vehicle.last_update_time = time.monotonic() - 1.0  # Simulate 1 second has passed
    vehicle.update()
    state = vehicle.get_state()

    assert state.throttle == -0.5
    assert state.speed < 0.0  # Speed should be negative for reverse


def test_reverse_braking():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = -5.0  # Simulate vehicle moving in reverse
    assert vehicle.get_state().speed == -5.0

    # Now apply brake while moving in reverse
    vehicle.set_brake(True)
    vehicle.last_update_time = time.monotonic() - 1.0  # Simulate another second has passed
    vehicle.update()
    state_after_brake = vehicle.get_state()

    assert state_after_brake.brake is True
    assert state_after_brake.speed == pytest.approx(0.0)


def test_reverse_coasting():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = -5.0
    assert vehicle.get_state().speed == -5.0
    vehicle.set_throttle(0.0)
    vehicle.set_brake(False)
    vehicle.last_update_time = time.monotonic() - 1.0
    vehicle.update()
    state_after_coast = vehicle.get_state()

    assert state_after_coast.speed == pytest.approx(-4.0)


def test_reverse_speed_limit():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.set_throttle(-1.0)  # Full reverse throttle
    vehicle.last_update_time = time.monotonic() - 6.0
    vehicle.update()
    state = vehicle.get_state()

    assert state.speed == pytest.approx(-vehicle.max_speed, abs=1e-2)

def test_acceleration_respects_elapsed_time():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.set_throttle(1.0)  # Full forward throttle
    vehicle.last_update_time = time.monotonic() - 1.0  # Simulate 2 seconds have passed
    vehicle.update()
    state = vehicle.get_state()

    expected_speed = min(vehicle.acceleration_rate * 1.0, vehicle.max_speed)
    assert state.speed == pytest.approx(expected_speed, abs=1e-2)

def test_acceleration_consistent_across_time_steps():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.set_throttle(1.0)  # Full forward throttle

    # Simulate two consecutive updates with 0.5s each
    vehicle.last_update_time = time.monotonic() - 0.5
    vehicle.update()
    speed_after_first_update = vehicle.get_state().speed

    # Advance relative to the timestamp set during the first update
    vehicle.last_update_time -= 0.5
    vehicle.update()
    speed_after_second_update = vehicle.get_state().speed

    expected_speed_after_first_update = min(vehicle.acceleration_rate * 0.5, vehicle.max_speed)
    expected_speed_after_second_update = min(vehicle.acceleration_rate * 1.0, vehicle.max_speed)

    assert speed_after_first_update == pytest.approx(expected_speed_after_first_update, abs=1e-2)
    assert speed_after_second_update == pytest.approx(expected_speed_after_second_update, abs=1e-2)

def test_acceleration_consistent_across_different_update_intervals():
    vehicle_a = SimulatedVehicle(command_timeout=10.0)
    vehicle_b = SimulatedVehicle(command_timeout=10.0)

    vehicle_a.set_throttle(1.0)
    vehicle_b.set_throttle(1.0)

    # Vehicle A: one 1.0s update
    vehicle_a.last_update_time = time.monotonic() - 1.0
    vehicle_a.update()
    speed_a = vehicle_a.get_state().speed

    # Vehicle B: two 0.5s updates
    vehicle_b.last_update_time = time.monotonic() - 0.5
    vehicle_b.update()
    vehicle_b.last_update_time -= 0.5
    vehicle_b.update()
    speed_b = vehicle_b.get_state().speed

    assert speed_a == pytest.approx(5.0, abs=1e-2)
    assert speed_b == pytest.approx(5.0, abs=1e-2)
    assert speed_b == pytest.approx(speed_a, abs=1e-2)

def test_zero_steering_keeps_heading_unchanged():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = 2.0
    vehicle.set_steering(0.0)
    vehicle.last_update_time = time.monotonic() - 0.5

    initial_heading = vehicle.heading
    vehicle.update()

    assert vehicle.heading == pytest.approx(initial_heading, abs=1e-6)


def test_positive_steering_while_moving_forward():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = 2.0
    vehicle.set_steering(1.0)
    vehicle.last_update_time = time.monotonic() - 0.5

    initial_heading = vehicle.heading
    vehicle.update()

    assert vehicle.heading < initial_heading


def test_negative_steering_while_moving_forward():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = 2.0
    vehicle.set_steering(-1.0)
    vehicle.last_update_time = time.monotonic() - 0.5

    initial_heading = vehicle.heading
    vehicle.update()

    assert vehicle.heading > initial_heading


def test_steering_does_not_change_heading_when_stationary():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = 0.0
    vehicle.set_steering(1.0)
    vehicle.last_update_time = time.monotonic() - 0.5

    initial_heading = vehicle.heading
    vehicle.update()

    assert vehicle.heading == pytest.approx(initial_heading, abs=1e-6)


def test_heading_always_remains_within_bounds():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = 2.0
    vehicle.set_steering(1.0)
    vehicle.last_update_time = time.monotonic() - 5.0

    for _ in range(100):
        vehicle.update()
        assert -math.pi <= vehicle.heading <= math.pi

def test_positive_steering_while_reverse():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = -2.0
    vehicle.set_steering(1.0)
    vehicle.last_update_time = time.monotonic() - 0.5

    initial_heading = vehicle.heading
    vehicle.update()

    assert vehicle.heading > initial_heading

def test_negative_steering_while_reverse():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = -2.0
    vehicle.set_steering(-1.0)
    vehicle.last_update_time = time.monotonic() - 0.5

    initial_heading = vehicle.heading
    vehicle.update()

    assert vehicle.heading < initial_heading    

def test_position_updates_when_moving_straight():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = 2.0
    vehicle.set_steering(0.0)
    vehicle.last_update_time = time.monotonic() - 1.0

    initial_x = vehicle.x
    initial_y = vehicle.y
    vehicle.update()

    assert vehicle.x > initial_x
    assert vehicle.y == pytest.approx(initial_y, abs=1e-6)
    assert vehicle.x - initial_x == pytest.approx(2.0, abs=1e-2)

def test_position_updates_when_heading_is_90_degrees():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = 2.0
    vehicle.heading = math.pi / 2  # 90 degrees
    vehicle.set_steering(0.0)
    vehicle.last_update_time = time.monotonic() - 1.0

    initial_x = vehicle.x
    initial_y = vehicle.y
    vehicle.update()

    assert vehicle.x == pytest.approx(initial_x, abs=1e-6)
    assert vehicle.y > initial_y
    assert vehicle.y - initial_y == pytest.approx(2.0, abs=1e-2)

def test_position_updates_when_heading_is_45_degrees():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = 2.0
    vehicle.heading = math.pi / 4  # 45 degrees
    vehicle.set_steering(0.0)
    vehicle.last_update_time = time.monotonic() - 1.0

    initial_x = vehicle.x
    initial_y = vehicle.y
    vehicle.update()

    expected_delta = 2.0 / math.sqrt(2)  # Since speed is along the diagonal
    assert vehicle.x - initial_x == pytest.approx(expected_delta, abs=1e-2)
    assert vehicle.y - initial_y == pytest.approx(expected_delta, abs=1e-2)

def test_position_updates_when_moving_in_reverse_at_45_degrees():
    vehicle = SimulatedVehicle(command_timeout=10.0)
    vehicle.speed = -2.0
    vehicle.heading = math.pi / 4  # 45 degrees
    vehicle.set_steering(0.0)
    vehicle.last_update_time = time.monotonic() - 1.0

    initial_x = vehicle.x
    initial_y = vehicle.y
    vehicle.update()

    expected_delta = -2.0 / math.sqrt(2)  # Since speed is along the diagonal in reverse
    assert vehicle.x - initial_x == pytest.approx(expected_delta, abs=1e-2)
    assert vehicle.y - initial_y == pytest.approx(expected_delta, abs=1e-2)

def test_position_updates_while_vehicle_is_turning():
    vehicle = SimulatedVehicle()
    initial_x = vehicle.x
    initial_y = vehicle.y

    vehicle.speed = 2.0
    vehicle.set_steering(0.5)
    vehicle._heartbeat()

    time.sleep(1.0)
    vehicle.update()

    assert vehicle.x > initial_x
    assert vehicle.y < initial_y
    assert vehicle.heading < 0.0