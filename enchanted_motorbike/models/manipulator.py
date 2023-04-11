from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field


class ManipulatorStateDecision(BaseModel):
    made_at: datetime = Field(...)
    state: Literal["TopRight", "TopLeft", "BottomRight", "BottomLeft"] = Field(...)
