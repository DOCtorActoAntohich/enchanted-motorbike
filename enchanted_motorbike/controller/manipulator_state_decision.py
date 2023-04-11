import asyncio
import logging

import fastapi_utils.tasks

from enchanted_motorbike.models import ManipulatorPosition, ManipulatorStateDecision
from enchanted_motorbike.settings import settings
from enchanted_motorbike.time import utc_time_now


@fastapi_utils.tasks.repeat_every(
    seconds=settings.controller.decision_interval_seconds, wait_first=True
)
async def decide_manipulator_state() -> None:
    new_state = await _get_new_state()
    logging.critical(f"decided {new_state}")
    state_decision = ManipulatorStateDecision(made_at=utc_time_now(), state=new_state)
    await _send_to_manipulator(state_decision)


async def _get_new_state() -> ManipulatorPosition:
    return ManipulatorPosition.TopRight


async def _send_to_manipulator(decision: ManipulatorStateDecision) -> None:
    reader, writer = await asyncio.open_connection(
        settings.manipulator.host, settings.manipulator.port
    )

    writer.write(decision.json().encode("utf-8"))
    await writer.drain()

    writer.close()
    await writer.wait_closed()
