import socket

from fastapi import FastAPI
import uvicorn

from enchanted_motorbike.models import SensorData
from enchanted_motorbike.settings import settings

app = FastAPI()


@app.get("/")
async def home():
    return "henlo"


@app.post("/sensor-data")
async def post_sensor_data(sensor_data: SensorData) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(settings.manipulator.address)
        sock.sendall(sensor_data.json().encode())


@app.get("/history")
async def get_history():
    ...


def run_controller() -> None:
    uvicorn.run(app, host="0.0.0.0", port=settings.controller.port, log_level="warning")
