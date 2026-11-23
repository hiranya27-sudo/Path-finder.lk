# Database

The database baseline uses PostgreSQL 16 with the pgvector extension. Phase 2
adds ingestion and review workflow support incrementally.

## Phase 1 and Phase 2 files

The repo is aligned with the updated roadmap v3 for Phase 1 (Weeks 1–3):

- `migrations/001_initial_schema.sql` creates the relational schema, vector
  columns, HNSW indexes, and the demand-snapshot refresh function.
- `migrations/002_phase2_ingestion_review.sql` adds ingestion-run tracking,
  source-event observations for the rolling skill review threshold, an
  admin-review audit table, and append-only resume/GitHub consent events.
- `seeds/001_initial_taxonomy.sql` inserts the draft technical skills, aliases,
  roles, and role-to-skill requirements.
- The database layer supports `jobs`, `skills`, `skill_aliases`,
  `skill_candidates`, `job_roles`, and `skill_demand` as the Phase 1 evidence
  foundation, with additional Phase 2 ingestion/review records.

The schema also anticipates the later review workflow in which unnormalized terms
are staged in `skill_candidates` and approved by a human-in-the-loop admin queue
before being promoted into the canonical taxonomy.

The Phase 2 migration creates `skill_candidate_review_queue`, which reports the
number of observations in the last 30 days and whether the term meets the
roadmap threshold of five observations. Resume and GitHub observations must use
opaque event keys and must not store raw documents, repository credentials, or
access tokens. Live collection remains disabled until an approved source and
access method are selected. Fixture rows are marked with `jobs.is_fixture` and
excluded from market-demand calculations.

The seed is safe to reapply: it uses the declared unique keys and
`ON CONFLICT` handling. Review the draft taxonomy with local experts before
using it as ground truth.

## Data-model notes

- `job_skills` links canonical technical skills to extracted job requirements;
  it is the evidence used to calculate local demand.
- `skill_demand.demand_score` is `D_s = job_count / total_jobs`. The initial
  taxonomy seed starts at zero because no vacancy evidence is supplied.
- `refresh_skill_demand()` updates all demand rows from non-expired,
  non-fixture jobs. The fixture ingestion task invokes it after successful
  batches; live collection is not enabled yet.
- Job and role embeddings use 384 dimensions as specified by the project
  documents. A concrete Sentence-BERT model still needs to be selected and
  validated.
- Proficiency is stored from 0 to 5; a role's required proficiency is 1 to 5.
- The database stores a resume storage key, not uploaded resume contents.
  Storage provider, consent flow, retention, and deletion policy must be agreed
  before resume ingestion is implemented.

## Apply scripts

From `it-career-system/`, with the Compose database healthy:

```powershell
Get-Content .\database\migrations\001_initial_schema.sql |
  docker compose exec -T db psql -U career_app -d career_system
Get-Content .\database\migrations\002_phase2_ingestion_review.sql |
  docker compose exec -T db psql -U career_app -d career_system
Get-Content .\database\seeds\001_initial_taxonomy.sql |
  docker compose exec -T db psql -U career_app -d career_system
```

Use the PostgreSQL username and database configured in `.env` if you changed
the defaults.
