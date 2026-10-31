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
    assert state.brake is False
    assert state.speed == 0.0
    assert state.throttle == 0.0

    vehicle.set_throttle(0.5)
    updated_state = vehicle.get_state()
    assert updated_state.throttle == 0.5