import enum
from datetime import datetime

from pydantic import BaseModel, Field


class ManipulatorPosition(enum.Enum):
    TopRight = enum.auto()
    TopLeft = enum.auto()
    BottomRight = enum.auto()
    BottomLeft = enum.auto()


class ManipulatorStateDecision(BaseModel):
    made_at: datetime = Field(...)
    state: ManipulatorPosition = Field(...)
