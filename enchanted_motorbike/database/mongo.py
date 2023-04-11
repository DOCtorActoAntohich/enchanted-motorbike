from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from enchanted_motorbike.settings import settings

_client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo.url)
_database: AsyncIOMotorDatabase = _client.get_database("enchanted_motorbike")
_sensor_data_collection: AsyncIOMotorCollection = _database.get_collection(
    "sensor_data"
)
_manipulator_states_collection: AsyncIOMotorCollection = _database.get_collection(
    "manipulator_states"
)


def get_sensor_data_collection() -> AsyncIOMotorCollection:
    return _sensor_data_collection


def get_manipulator_states_collection() -> AsyncIOMotorCollection:
    return _manipulator_states_collection
