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