import uvicorn
from fastapi import Depends, FastAPI

from enchanted_motorbike.controller.manipulator_state_decision import (
    decide_manipulator_state,
)
from enchanted_motorbike.database import SensorDataCollection
from enchanted_motorbike.models import SensorData
from enchanted_motorbike.settings import settings

app = FastAPI()


@app.post("/sensor-data")
async def post_sensor_data(
    sensor_data: SensorData,
    collection: SensorDataCollection = Depends(SensorDataCollection.create),
) -> None:
    await collection.save(sensor_data)


@app.get("/history")
async def get_history() -> None:
    raise NotImplementedError


@app.on_event("startup")
async def on_startup() -> None:
    await decide_manipulator_state()


def run_controller() -> None:
    uvicorn.run(app, host="", port=settings.controller.port, log_level="warning")
