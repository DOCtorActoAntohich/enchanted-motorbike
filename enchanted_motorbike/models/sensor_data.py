from datetime import datetime

from pydantic import BaseModel, Field


class SensorData(BaseModel):
    observed_at: datetime = Field(...)
    x: int = Field()
    y: int = Field()

    class Config:
        json_encoders = {
            datetime: lambda d: d.isoformat()
        }
