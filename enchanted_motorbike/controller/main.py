from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI

from enchanted_motorbike.controller.manipulator_state_decision import (
    decide_manipulator_state,
)
from enchanted_motorbike.database import SensorDataRepository, ManipulatorStatesRepository
from enchanted_motorbike.models import SensorData, ManipulatorStateDecision
from enchanted_motorbike.settings import settings

app = FastAPI()


@app.post("/sensor-data")
async def post_sensor_data(
        sensor_data: SensorData,
        repository: SensorDataRepository = Depends(SensorDataRepository.create),
) -> None:
    await repository.save(sensor_data)


@app.get("/history")
async def get_history(
        after: datetime | None,
        before: datetime | None,
        repository: ManipulatorStatesRepository = Depends(ManipulatorStatesRepository.create),
) -> list[ManipulatorStateDecision]:
    return await repository.history(after=after, before=before)


@app.on_event("startup")
async def on_startup() -> None:
    await decide_manipulator_state()


def run_controller() -> None:
    uvicorn.run(app, host="", port=settings.controller.port, log_level="warning")
