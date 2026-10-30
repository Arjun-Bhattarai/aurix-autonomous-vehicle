from pydantic import BaseModel, Field


class VehicleCommand(BaseModel):
    steering: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Steering angle between -1.0 (left) and 1.0 (right)"
    )

    throttle: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Throttle between -1.0 (reverse) and 1.0 (forward)"
    )

    brake: bool = Field(default=False, description="True if the brake is engaged, False otherwise")