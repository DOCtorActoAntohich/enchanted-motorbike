from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ManipulatorStateDecision(BaseModel):
    made_at: datetime = Field(...)
    state: Literal["TopRight", "TopLeft", "BottomRight", "BottomLeft"] = Field(...)
