import asyncio
from datetime import datetime
import subprocess

from fastapi import Depends, FastAPI

from enchanted_motorbike.controller.manipulator_state_decision import (
    decide_manipulator_state, run_decider_thing
)
from enchanted_motorbike.database import SensorDataRepository, ManipulatorStatesRepository
from enchanted_motorbike.models import SensorData, ManipulatorStateDecision

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
    proc = subprocess.Popen([
        "gunicorn",
        "enchanted_motorbike.controller.main:app",
        "--workers",
        "4",
        "--worker-class",
        "uvicorn.workers.UvicornWorker",
        "--bind",
        "0.0.0.0:8000"
    ])

    asyncio.run(run_decider_thing())

    proc.kill()
