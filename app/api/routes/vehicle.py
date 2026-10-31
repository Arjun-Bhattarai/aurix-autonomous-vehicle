from fastapi import APIRouter, Depends

from app.vehicle.simulator import SimulatedVehicle
from app.vehicle.interface import VehicleInterface
from app.schemas.telemetry import VehicleTelemetry
from app.schemas.commands import VehicleCommand


router = APIRouter()

_shared_vehicle = SimulatedVehicle()

def get_vehicle() -> VehicleInterface:
    """Provides the shared vehicle instance for dependency injection."""
    return _shared_vehicle


@router.get("/state", response_model=VehicleTelemetry)
def get_vehicle_state(vehicle: VehicleInterface = Depends(get_vehicle)):
    """Get the current state of the vehicle."""
    return vehicle.get_state()


@router.post("/control", response_model=VehicleTelemetry)
def control_vehicle(command: VehicleCommand, vehicle: VehicleInterface = Depends(get_vehicle)):
    """Control the vehicle using the provided command."""
    vehicle.set_steering(command.steering)
    vehicle.set_brake(command.brake)
    vehicle.set_throttle(command.throttle)

    return vehicle.get_state()


@router.post("/emergency-stop", response_model=VehicleTelemetry)
def emergency_stop(vehicle: VehicleInterface = Depends(get_vehicle)):
    """Trigger an emergency stop for the vehicle."""
    vehicle.emergency_stop()
    return vehicle.get_state()


@router.post("/reset-emergency-stop", response_model=VehicleTelemetry)
def reset_emergency_stop(vehicle: VehicleInterface = Depends(get_vehicle)):
    """Reset the emergency stop state of the vehicle."""
    vehicle.reset_emergency_stop()
    return vehicle.get_state()