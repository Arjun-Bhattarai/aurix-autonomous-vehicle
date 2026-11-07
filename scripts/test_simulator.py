import time

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
    assert state.brake is False      # Brake is released on reset
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
    assert state.is_connected is False
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
    
    # Make last_command_time stale
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
