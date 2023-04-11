import asyncio
import logging
import time
import random

import httpx
from tqdm import tqdm

from enchanted_motorbike.models import SensorData
from enchanted_motorbike.settings import settings
from enchanted_motorbike.time import utc_time_now

MaxParallelRequests = 32


def random_position() -> int:
    return random.randint(-100, 100)  # noqa: S311


def random_data_sample() -> SensorData:
    return SensorData(
        observed_at=utc_time_now(), x=random_position(), y=random_position()
    )


async def send_request(client: httpx.AsyncClient, url: str, content: str) -> None:
    await client.post(url, content=content)


async def send_requests() -> None:
    client = httpx.AsyncClient()
    url = f"{settings.controller.full_hostname}/sensor-data"
    tasks: list[asyncio.Task] = [
        asyncio.create_task(send_request(client, url, random_data_sample().json()))
        for _ in range(MaxParallelRequests)
    ]
    progress_bar = tqdm()
    while True:
        for i, task in enumerate(tasks):
            if task.done():
                tasks[i] = asyncio.create_task(send_request(client, url, random_data_sample().json()))
                await task
                progress_bar.update()
                progress_bar.set_description("\n")
        await asyncio.sleep(0.1)


def run_sensor() -> None:
    asyncio.run(send_requests())
