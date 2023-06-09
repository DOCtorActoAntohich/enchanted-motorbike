import asyncio
from datetime import datetime, timedelta

from enchanted_motorbike.database import (
    ManipulatorStatesRepository,
    SensorDataRepository,
)
from enchanted_motorbike.models import ManipulatorStateDecision
from enchanted_motorbike.settings import settings
from enchanted_motorbike.time import utc_time_now


async def run_decider_thing() -> None:
    while True:
        await asyncio.sleep(settings.controller.decision_interval_seconds)
        await decide_manipulator_state()


async def decide_manipulator_state() -> None:
    manipulator_repository = ManipulatorStatesRepository.create()
    latest_decision = await manipulator_repository.latest()

    time_now = utc_time_now()
    new_state = await _calculate_new_state(
        after=latest_decision.made_at
        if latest_decision is not None
        else time_now
        - timedelta(seconds=2 * settings.controller.decision_interval_seconds),
        before=time_now,
    )
    if new_state is None:
        return
    new_decision = ManipulatorStateDecision(made_at=time_now, state=new_state)

    if latest_decision is None or new_decision.state != latest_decision.state:
        await manipulator_repository.save(new_decision)

    await _send_to_manipulator(new_decision)


async def _calculate_new_state(after: datetime, before: datetime) -> str | None:
    sensor_repository = SensorDataRepository.create()
    data = await sensor_repository.average(after, before)
    if data is None:
        return None

    x, y = data

    await sensor_repository.delete_all_before(before)

    if x < 0 and y < 0:
        return "BottomLeft"
    if x < 0 and y >= 0:
        return "TopLeft"
    if x >= 0 and y < 0:
        return "BottomRight"
    return "TopRight"


async def _send_to_manipulator(decision: ManipulatorStateDecision) -> None:
    reader, writer = await asyncio.open_connection(
        settings.manipulator.host, settings.manipulator.port
    )

    writer.write(decision.json().encode("utf-8"))
    await writer.drain()

    writer.close()
    await writer.wait_closed()
