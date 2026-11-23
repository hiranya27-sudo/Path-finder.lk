# Explainable AI Career System

A decision-support system for Sri Lankan IT undergraduates that compares
technical skills with local IT roles and vacancies, prioritizes skill gaps,
and explains recommendations.

The project roadmap's core stack is retained:

- API: FastAPI
- Web: React + Vite
- Database: PostgreSQL 16 + pgvector
- Background ingestion: Celery + Redis
- Technical extraction: spaCy and PyGithub
- Recommendation and explainability: Sentence-BERT, scikit-learn, and SHAP

## Project layout

```text
it-career-system/
├── backend/                  # FastAPI API (later implementation phase)
├── database/
│   ├── migrations/           # PostgreSQL DDL
│   └── seeds/                # Initial draft role/skill taxonomy
├── docs/
│   └── phase-1/              # Scope, requirements, architecture, data dictionary
├── frontend/                 # React + Vite web application (later phase)
├── ml/                       # Recommendation and XAI modules (later phase)
├── tests/                    # Project-level validation and evaluation tests
└── worker/                   # Celery + Redis fixture ingestion worker
```

## Phase 1: Architecture and database foundation

This repository is aligned to the v3 16-week roadmap for the Sri Lankan IT career
system. Phase 1 is the foundation phase (Weeks 1–3) and intentionally covers
scope definition, database modeling, and the initial taxonomy baseline only.

Phase 1 deliverables are in [`docs/phase-1/`](docs/phase-1/):

- Requirements, boundaries, personas, and acceptance criteria
- Technology architecture and data-flow diagram (Architecture v2)
- Relational schema and data dictionary for `jobs`, `skills`, `skill_aliases`,
  `skill_candidates`, `job_roles`, and `skill_demand`
- A 44-skill / 19-role draft technical taxonomy
- PostgreSQL 16 + pgvector local setup

Phase 2 implementation has started with an incremental migration, local Redis
service, and a fixture-backed Celery ingestion task. Live vacancy crawling,
spaCy/PyGithub extraction, review APIs and screens, calibration UI, dynamic
role discovery, and the recommender remain incomplete.

The project plan specifies the taxonomy's size, not the names of its skills or
roles. The seed catalog is therefore a proposed starting point and needs
review by the supervisor and local-domain experts before being treated as an
approved research taxonomy.

## Start the local development stack

Requires Docker Desktop with Compose.

1. Copy `.env.example` to `.env` and set a private local database password.
2. Start PostgreSQL, Redis, and the worker:

   ```powershell
   docker compose up -d --build
   ```

3. Apply the schema, Phase 2 migration, and draft taxonomy:

   ```powershell
   Get-Content .\database\migrations\001_initial_schema.sql |
     docker compose exec -T db psql -U career_app -d career_system
   Get-Content .\database\migrations\002_phase2_ingestion_review.sql |
     docker compose exec -T db psql -U career_app -d career_system
   Get-Content .\database\seeds\001_initial_taxonomy.sql |
     docker compose exec -T db psql -U career_app -d career_system
   ```

   If you changed `POSTGRES_USER` or `POSTGRES_DB` in `.env`, substitute those
   values in the commands above.

4. Confirm the seeded catalog:

   ```powershell
   docker compose exec db psql -U career_app -d career_system -c `
     "SELECT count(*) AS skills FROM skills; SELECT count(*) AS roles FROM job_roles;"
   ```

5. Exercise the fixture-only ingestion task:

   ```powershell
   docker compose exec worker celery -A career_worker.celery_app:app call `
     career_worker.tasks.ingest_fixture_jobs
   ```

Fixture postings are synthetic test data and are excluded from market-demand
calculations. Live collection is disabled until an approved vacancy source and
access method are selected.

The database listens on `127.0.0.1:5432`. The Compose file does not publish
PostgreSQL on external network interfaces. Local development credentials and
database contents are not production security settings.

For detailed schema and setup notes, see [`database/README.md`](database/README.md).

## Phase boundaries

This repository contains the Phase 1 design and initial Phase 2 ingestion
scaffold. It does not yet implement live-job crawling, resume/GitHub
extraction, review/calibration interfaces, recommendation models, SHAP
explanations, or production deployment.
