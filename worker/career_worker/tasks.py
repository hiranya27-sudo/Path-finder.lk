import os
from pathlib import Path

import psycopg

from career_worker.celery_app import app
from career_worker.ingestion import ingest_fixture_batch, load_fixture_jobs
from career_worker.ingestion import FixtureJobSource, ingest_job_source

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "jobs.json"


def _database_connection() -> psycopg.Connection:
    required = ("POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "Missing required database environment variables: " + ", ".join(missing)
        )
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=10,
    )


FIXTURE_SOURCE = FixtureJobSource(Path(__file__).parent / "fixtures" / "jobs.json")


@app.task(
    name="career_worker.tasks.ingest_fixture_jobs",
    autoretry_for=(psycopg.OperationalError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def ingest_fixture_jobs() -> dict[str, int | str]:
    with _database_connection() as connection:
        result = ingest_job_source(connection, FIXTURE_SOURCE)
    return {
        "source": result.source,
        "ingestion_run_id": result.ingestion_run_id,
        "jobs_seen": result.jobs_seen,
        "jobs_inserted": result.jobs_inserted,
        "jobs_updated": result.jobs_updated,
    }
