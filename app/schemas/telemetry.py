from typing import Literal
from pydantic import BaseModel, Field


class VehicleTelemetry(BaseModel):
    speed: float = Field(ge=-100.0, le=100.0, description="Vehicle speed in meters per second")
    steering: float = Field(ge=-1.0, le=1.0, description="Steering angle between -1.0 (left) and 1.0 (right)")
    throttle: float = Field(ge=-1.0, le=1.0, description="Throttle between -1.0 (reverse) and 1.0 (forward)")
    brake: bool = Field(default=False, description="True if the brake is engaged, False otherwise")
    is_connected: bool = Field(default=False, description="True if the vehicle is connected, False otherwise")
    mode: Literal["simulation", "hardware"]
    emergency_stopped: bool = Field(default=False, description="True if the vehicle is in an emergency stop state, False otherwise")
    communication_timed_out: bool = Field(default=False, description="True if the vehicle has experienced a communication timeout, False otherwise")