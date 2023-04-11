import asyncio
import random

import httpx
from tqdm import tqdm

from enchanted_motorbike.models import SensorData
from enchanted_motorbike.settings import settings
from enchanted_motorbike.time import utc_time_now


class Sensor:
    MaxParallelRequests = 32

    __client = httpx.AsyncClient()
    __url = f"{settings.controller.full_hostname}/sensor-data"

    @classmethod
    def run(cls) -> None:
        asyncio.run(cls.generate_data_infinitely())

    @classmethod
    async def generate_data_infinitely(cls) -> None:
        tasks: list[asyncio.Task] = [
            cls.__create_request_task() for _ in range(cls.MaxParallelRequests)
        ]
        progress_bar = tqdm()  # shows rps

        while True:
            for i, task in enumerate(tasks):
                if not task.done():
                    continue
                tasks[i] = cls.__create_request_task()
                await task
                progress_bar.update()
                progress_bar.set_description("\n")  # to display properly
            await asyncio.sleep(0.1)

    @classmethod
    def __create_request_task(cls) -> asyncio.Task:
        return asyncio.create_task(
            cls.__client.post(cls.__url, content=cls.random_data_sample().json())
        )

    @classmethod
    def __random_position(cls) -> int:
        return random.randint(-100, 100)  # noqa: S311

    @classmethod
    def random_data_sample(cls) -> SensorData:
        return SensorData(
            observed_at=utc_time_now(),
            x=cls.__random_position(),
            y=cls.__random_position(),
        )
