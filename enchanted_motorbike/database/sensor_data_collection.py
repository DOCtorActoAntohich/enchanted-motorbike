from __future__ import annotations

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor

from enchanted_motorbike.database.mongo import get_sensor_data_collection
from enchanted_motorbike.models import SensorData


class SensorDataCollection:
    @classmethod
    def create(cls) -> SensorDataCollection:
        return cls(get_sensor_data_collection())

    def __init__(self, motor_collection: AsyncIOMotorCollection) -> None:
        self.__collection = motor_collection

    async def save(self, sensor_data: SensorData) -> None:
        self.__collection.insert_one(sensor_data.dict())

    def get_all_before(self, date: datetime) -> AsyncIOMotorCursor:
        return self.__collection.find({"observed_at": {"$lte": date}}).sort(
            "observed_at", 1
        )
