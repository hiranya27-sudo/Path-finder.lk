from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol


logger = logging.getLogger(__name__)


class Cursor(Protocol):
    def execute(
        self, query: str, params: tuple[object, ...] | None = None
    ) -> Cursor: ...

    def fetchone(self) -> tuple[object, ...] | None: ...

    def __enter__(self) -> Cursor: ...

    def __exit__(self, *args: object) -> None: ...


class Connection(Protocol):
    def cursor(self) -> Cursor: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


@dataclass(frozen=True)
class JobPosting:
    source_job_id: str
    title: str
    description: str
    source_url: str | None = None
    company: str | None = None
    location: str | None = None
    posted_at: datetime | None = None
    expires_at: datetime | None = None


@dataclass(frozen=True)
class IngestionResult:
    source: str
    ingestion_run_id: int
    jobs_seen: int
    jobs_inserted: int
    jobs_updated: int


def _optional_timestamp(value: object, field: str) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 string or null")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{field} must be a valid ISO-8601 timestamp") from error
    if parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone")
    return parsed


def _required_text(record: dict[str, object], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def load_fixture_jobs(path: Path) -> list[JobPosting]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to load fixture jobs from {path}") from error
    if not isinstance(document, list):
        raise ValueError("Fixture data must be a JSON array")

    jobs: list[JobPosting] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(document):
        if not isinstance(item, dict):
            raise ValueError(f"Fixture record {index} must be an object")
        source_job_id = _required_text(item, "source_job_id")
        if source_job_id in seen_ids:
            raise ValueError(f"Duplicate fixture source_job_id: {source_job_id}")
        seen_ids.add(source_job_id)

        optional_fields: dict[str, str | None] = {}
        for field in ("source_url", "company", "location"):
            value = item.get(field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{field} must be a non-empty string or null")
            optional_fields[field] = value.strip() if isinstance(value, str) else None

        jobs.append(
            JobPosting(
                source_job_id=source_job_id,
                title=_required_text(item, "title"),
                description=_required_text(item, "description"),
                source_url=optional_fields["source_url"],
                company=optional_fields["company"],
                location=optional_fields["location"],
                posted_at=_optional_timestamp(item.get("posted_at"), "posted_at"),
                expires_at=_optional_timestamp(item.get("expires_at"), "expires_at"),
            )
        )
    return jobs


_SOURCE_KEY = re.compile(r"^[a-z0-9][a-z0-9_-]{0,62}$")


class JobSource(Protocol):
    source_key: str
    is_fixture: bool

    def fetch_jobs(self) -> list[JobPosting]: ...


def validate_source_key(source_key: str) -> str:
    if not isinstance(source_key, str) or not _SOURCE_KEY.fullmatch(source_key):
        raise ValueError(
            "source_key must be a lowercase slug using letters, numbers, "
            "hyphens, or underscores"
        )
    return source_key


@dataclass(frozen=True)
class FixtureJobSource:
    path: Path
    source_key: str = "fixture"
    is_fixture: bool = True

    def fetch_jobs(self) -> list[JobPosting]:
        return load_fixture_jobs(self.path)


def _mark_failed(
    connection: Connection,
    ingestion_run_id: int,
    error_code: str,
) -> None:
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingestion_runs
                   SET status = 'failed',
                       completed_at = now(),
                       error_code = %s
                 WHERE ingestion_run_id = %s
                """,
                (error_code[:100], ingestion_run_id),
            )
        connection.commit()
    except Exception:
        connection.rollback()
        logger.exception("Could not record failed ingestion run %s", ingestion_run_id)
        raise


def ingest_job_source(
    connection: Connection,
    source: JobSource,
) -> IngestionResult:
    source_key = validate_source_key(source.source_key)
    if not isinstance(source.is_fixture, bool):
        raise ValueError("source.is_fixture must be a boolean")

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO ingestion_runs (source)
            VALUES (%s)
            RETURNING ingestion_run_id
            """,
            (source_key,),
        )
        row = cursor.fetchone()
        if row is None:
            raise RuntimeError("Database did not return an ingestion run ID")
        ingestion_run_id = int(row[0])
    connection.commit()

    inserted = 0
    updated = 0

    try:
        jobs = source.fetch_jobs()
        if not isinstance(jobs, list):
            raise TypeError("A job source must return a list of JobPosting values")

        seen_ids: set[str] = set()
        for job in jobs:
            if not isinstance(job, JobPosting):
                raise TypeError("A job source returned a non-JobPosting value")
            if not job.source_job_id or job.source_job_id != job.source_job_id.strip():
                raise ValueError("source_job_id must be non-empty and trimmed")
            if job.source_job_id in seen_ids:
                raise ValueError(f"Duplicate source_job_id: {job.source_job_id}")
            seen_ids.add(job.source_job_id)
            if not job.title.strip() or not job.description.strip():
                raise ValueError("Job title and description must be non-empty")

        with connection.cursor() as cursor:
            for job in jobs:
                cursor.execute(
                    """
                    INSERT INTO jobs (
                        source,
                        source_job_id,
                        source_url,
                        title,
                        company,
                        location,
                        description,
                        posted_at,
                        expires_at,
                        is_fixture
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (source, source_job_id) DO NOTHING
                    RETURNING job_id
                    """,
                    (
                        source_key,
                        job.source_job_id,
                        job.source_url,
                        job.title,
                        job.company,
                        job.location,
                        job.description,
                        job.posted_at,
                        job.expires_at,
                        source.is_fixture,
                    ),
                )
                if cursor.fetchone() is not None:
                    inserted += 1
                    continue

                cursor.execute(
                    """
                    UPDATE jobs
                       SET source_url = %s,
                           title = %s,
                           company = %s,
                           location = %s,
                           description = %s,
                           posted_at = %s,
                           expires_at = %s,
                           collected_at = now(),
                           is_fixture = %s
                     WHERE source = %s AND source_job_id = %s
                    RETURNING job_id
                    """,
                    (
                        job.source_url,
                        job.title,
                        job.company,
                        job.location,
                        job.description,
                        job.posted_at,
                        job.expires_at,
                        source.is_fixture,
                        source_key,
                        job.source_job_id,
                    ),
                )
                if cursor.fetchone() is None:
                    raise RuntimeError(
                        f"Could not update source job {job.source_job_id}"
                    )
                updated += 1

            cursor.execute("SELECT refresh_skill_demand()")
            cursor.execute(
                """
                UPDATE ingestion_runs
                   SET status = 'succeeded',
                       completed_at = now(),
                       jobs_seen = %s,
                       jobs_inserted = %s,
                       jobs_updated = %s
                 WHERE ingestion_run_id = %s
                """,
                (len(jobs), inserted, updated, ingestion_run_id),
            )
        connection.commit()
    except Exception as error:
        connection.rollback()
        _mark_failed(connection, ingestion_run_id, type(error).__name__)
        raise

    return IngestionResult(
        source=source_key,
        ingestion_run_id=ingestion_run_id,
        jobs_seen=len(jobs),
        jobs_inserted=inserted,
        jobs_updated=updated,
    )
