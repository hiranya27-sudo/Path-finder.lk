# Phase 1 — Data Dictionary

The authoritative DDL is
[`001_initial_schema.sql`](../../database/migrations/001_initial_schema.sql).
This document summarizes the intended entities.

| Entity | Purpose | Important integrity rules |
| --- | --- | --- |
| `jobs` | Source-attributed local IT vacancy snapshots | Source and title required; source identifier unique within a source; optional expiry and 384-d embedding |
| `skills` | Canonical technical skill catalog | Unique canonical name and domain cluster |
| `skill_aliases` | Raw spellings mapped to canonical skills | Case-insensitive unique raw term; each alias references one canonical skill |
| `skill_candidates` | Newly discovered terms awaiting taxonomy review | Positive observation count; pending/approved/rejected/merged states |
| `job_roles` | IT career role catalog | Unique title; optional 384-d role vector |
| `role_skills` | Skill proficiency and importance required by a role | Required level 1–5; positive importance weight |
| `job_skills` | Extracted skill evidence on a vacancy | One row per job/skill; extraction method and optional confidence 0–1 |
| `skill_demand` | Timestamped local-demand snapshot per skill | Job count cannot exceed eligible-job denominator; score 0–1 |
| `student_profiles` | Candidate profile and source references | Unique email; CV reference is an opaque storage key |
| `student_skills` | Candidate skill proficiency with provenance | Proficiency 0–5; source is self-report, resume, GitHub, or advisor |

## Demand snapshot

The schema's `refresh_skill_demand()` function counts distinct non-expired jobs
with evidence for each canonical skill and persists:

```text
D_s = job_count / total_jobs
```

When there are no eligible jobs, both counts and demand score remain zero. A
zero score at that point means “no evidence loaded,” not “no local demand.”

## Skill gap

The downstream gap calculation is:

```text
Gap(s) = W_type × D_s × (1 - P_s / 5)
```

`P_s` is the candidate proficiency, `D_s` is the market-demand snapshot, and
`W_type` is stored as the role-skill `importance_weight`. The project must not
conflate a missing assessment with a measured proficiency of zero; the future
API should represent unassessed skills separately.
