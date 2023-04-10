import asyncio

import httpx
import random
from datetime import datetime, timezone

from enchanted_motorbike.models import SensorData
from enchanted_motorbike.settings import settings


def random_position() -> int:
    return random.randint(-100, 100)


def random_data_sample() -> SensorData:
    return SensorData(
        observed_at=datetime.now(tz=timezone.utc),
        x=random_position(),
        y=random_position()
    )


async def send_bagillion_requests() -> None:
    async with httpx.AsyncClient() as client:
        while True:
            await client.post(
                f"{settings.controller.full_hostname}/sensor-data",
                content=random_data_sample().json()
            )
            await asyncio.sleep(1)


async def run():
    try:
        await send_bagillion_requests()
    except KeyboardInterrupt:
        return


def run_sensor() -> None:
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(run())
    except KeyboardInterrupt:
        return
