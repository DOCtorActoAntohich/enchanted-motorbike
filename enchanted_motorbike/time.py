from datetime import datetime, timezone


def utc_time_now() -> datetime:
    return datetime.now(tz=timezone.utc)
