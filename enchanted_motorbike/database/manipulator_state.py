from __future__ import annotations

from datetime import datetime

from pydantic import parse_obj_as
from motor.motor_asyncio import AsyncIOMotorCollection

from enchanted_motorbike.models import ManipulatorStateDecision
from enchanted_motorbike.database.mongo import get_manipulator_states_collection


class ManipulatorStatesRepository:
    @classmethod
    def create(cls) -> ManipulatorStatesRepository:
        return cls(get_manipulator_states_collection())

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.__collection = collection

    async def save(self, decision: ManipulatorStateDecision) -> None:
        self.__collection.insert_one(decision.dict())

    async def latest(self) -> ManipulatorStateDecision | None:
        async for item in self.__collection.find().sort("made_at", -1).limit(1):
            return parse_obj_as(ManipulatorStateDecision, item)
        return None

    async def history(
            self,
            *,
            after: datetime | None = None,
            before: datetime | None = None
    ) -> list[ManipulatorStateDecision]:
        request = self.__history_request(after, before)
        if request is None:
            return await self.last_n(100)

        items = await self.__collection.find(request).sort("made_at", 1).to_list(length=None)
        return self.__parse_list(items)

    async def last_n(self, n: int) -> list[ManipulatorStateDecision]:
        items = await self.__collection.find().sort("made_at", -1).limit(n).to_list(length=n)
        items.reverse()
        return self.__parse_list(items)

    @classmethod
    def __history_request(cls, after: datetime | None, before: datetime | None) -> dict | None:
        conditions = {}
        if after is not None:
            conditions["$gte"] = after
        if before is not None:
            conditions["$lte"] = before
        if len(conditions) == 0:
            return None
        return {"made_at": conditions}

    @classmethod
    def __parse_list(cls, items: list) -> list[ManipulatorStateDecision]:
        return [
            parse_obj_as(ManipulatorStateDecision, item)
            for item in items
        ]
