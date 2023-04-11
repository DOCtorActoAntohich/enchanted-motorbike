from __future__ import annotations

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor

from enchanted_motorbike.database.mongo import get_sensor_data_collection
from enchanted_motorbike.models import SensorData


class SensorDataRepository:
    @classmethod
    def create(cls) -> SensorDataRepository:
        return cls(get_sensor_data_collection())

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.__collection = collection

    async def save(self, sensor_data: SensorData) -> None:
        await self.__collection.insert_one(sensor_data.dict())

    def get_all_before(self, date: datetime) -> AsyncIOMotorCursor:
        return self.__collection.find({"observed_at": {"$lte": date}}).sort(
            "observed_at", 1
        )

    async def delete_all_before(self, date: datetime) -> int:
        result = await self.__collection.delete_many({"observed_at": {"$lte": date}})
        return result.deleted_count

    async def average(self, after: datetime, before: datetime) -> tuple[float, float] | None:
        stage_filter = {
            "$match": {
                "observed_at": {"$gte": after, "$lte": before}
            }
        }
        stage_group = {
            "$group": {
                "_id": {"$sum": 1},
                "x": {"$avg": "$x"},
                "y": {"$avg": "$y"}
            }
        }
        pipeline = [stage_filter, stage_group]
        try:
            result, *_ = await self.__collection.aggregate(pipeline).to_list(length=None)
        except ValueError:
            return None
        return result["x"], result["y"]
