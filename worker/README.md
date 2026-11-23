# Background workers

Phase 2 adds a Celery worker backed by Redis. The first task deliberately uses
fixture vacancies only; live collection stays disabled until an approved
vacancy source and access method are selected.

## Run locally

1. Apply migrations `001_initial_schema.sql` and
   `002_phase2_ingestion_review.sql`, then apply the taxonomy seed.
2. Set `POSTGRES_PASSWORD` in `.env`.
3. Start local services with `docker compose up -d --build`.
4. Run the fixture ingestion task:

   ```powershell
   docker compose exec worker celery -A career_worker.celery_app:app call `
     career_worker.tasks.ingest_fixture_jobs
   ```

Fixture rows are marked `is_fixture` and excluded from demand snapshots. The
task is idempotent by `(source, source_job_id)` and records an ingestion run.
