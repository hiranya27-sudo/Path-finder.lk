import os

from celery import Celery


app = Celery(
    "career_worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
)
app.conf.update(
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
)

import career_worker.tasks  # noqa: E402,F401
