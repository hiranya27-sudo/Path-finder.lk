# Phase 1 — Requirements and Scope

## Project identity

**Working title:** Explainable AI-Based Career Recommendation, Skill Gap
Analysis, and Personalized Job Opportunity Discovery System for Sri Lankan IT
Undergraduates.

**Domain:** Sri Lankan IT-BPM employment market.

**Primary users:** IT undergraduates and recent graduates. Academic counselors
and employers are secondary stakeholders; their access and responsibilities
require confirmation before implementation.

## Problem

Undergraduates may have difficulty understanding how their technical skills
map to local IT job roles, which skills are most important to improve, and
which current local vacancies match their experience. Generic international
recommendations, unnormalized skill names, binary skill checklists, and
unexplained rankings do not adequately communicate local evidence or
uncertainty.

## Objectives

1. Create a timestamped knowledge base of Sri Lankan IT vacancies.
2. Normalize technical-skill names into an initial canonical taxonomy of 44
   skills across 19 IT roles.
3. Design for dual-source evidence: resume text parsing and GitHub repository
   metadata.
4. Represent candidate technical proficiency on a calibrated 0–5 scale.
5. Compare TF-IDF and Sentence-BERT similarity with a multi-factor
   recommendation approach.
6. Require at least 70% assessment coverage before ranking roles.
7. Resolve equal scores deterministically: assessment coverage, high-weight
   skill score, then alphabetical role title.
8. Prioritize technical skill gaps by local demand and role importance:
   `Gap(s) = W_type × D_s × (1 - P_s / 5)`.
9. Design explainability around feature attribution, SHAP analysis, and
   evidence-grounded explanations.
10. Plan evaluation against 10–15 expert-reviewed reference personas using
    Precision@K, Recall@K, and NDCG@K, plus a user trust/usability assessment.
11. Support personalized matching against active Sri Lankan IT vacancies.
12. Deliver a React + Vite interface backed by a FastAPI service.

## Roadmap alignment with the v3 plan

The updated development plan separates the work into a 16-week sequence. Phase 1
is the foundation stage and aligns to Weeks 1–3:

- System scope definition and user persona setup
- PostgreSQL 16 DDL schema for `Jobs`, `Skills`, `SkillAliases`,
  `SkillCandidates`, `JobRoles`, and `SkillDemand`
- `pgvector` HNSW configuration for 384-d embeddings
- A reviewable 44-skill / 19-role taxonomy baseline
- Verified schema and architecture artifacts for the data layer

The next roadmap phases add Celery + Redis ingestion, dual CV/GitHub extraction,
role discovery, hybrid recommendation, and evaluation. Those are intentionally
out of scope for this Phase 1 baseline.

## Scope

### In scope for the complete project

- Ingest and snapshot local IT vacancy data, subject to source terms and
  permission.
- Normalize technical terms to canonical skills and retain source evidence.
- Collect candidate-provided proficiency and, with consent, resume/GitHub
  evidence.
- Recommend technical career paths and explain the evidence behind the ranking.
- Rank current vacancies by candidate/profile fit.
- Provide role/skill data maintenance and a human review queue for new terms.
- Evaluate recommendation ranking and user-facing explanations.

### In scope for this Phase 1 implementation

- Define project boundaries, stakeholders, requirements, and measurable
  acceptance criteria.
- Document the target stack and architecture.
- Create the initial PostgreSQL 16 schema and pgvector indexes.
- Seed a reviewable draft catalog of 44 technical skills and 19 roles, with
  aliases and role-skill requirements.
- Provide a local PostgreSQL + pgvector development setup.

### Out of scope for Phase 1

- Production vacancy crawling, Celery tasks, or Redis configuration.
- Resume upload/parsing, GitHub API calls, or spaCy extraction.
- Any recommendation model, Sentence-BERT inference, SHAP computation, or RAG.
- Candidate/admin UI, frontend, authentication, and authorization.
- Production hosting, external storage, and release/deployment automation.

These are later roadmap deliverables. The project directories are prepared for
them, but no feature-complete Phase 2 code is claimed.

## User personas

| Persona | Need | Phase 1 design consideration |
| --- | --- | --- |
| IT undergraduate | Understand role fit and improve relevant technical skills | Profile, skill evidence, proficiency, gaps, and understandable explanations |
| Recent graduate | Compare current readiness with local vacancies | Current, dated vacancy evidence and match rationale |
| Academic counselor | Help a student interpret career options | Counselor role and access rules require stakeholder approval |
| Employer / domain expert | Review role-skill expectations and advise on taxonomy | No access to candidate data without explicit authorization |
| Taxonomy administrator | Review newly discovered technical terms | Candidate terms are staged; approval must not silently alter canonical skills |

## Functional requirements

| ID | Requirement |
| --- | --- |
| FR-01 | Store vacancy source, source identifier, title, description, location, collection time, and optional posted/expiry times. |
| FR-02 | Store canonical technical skills, spelling/alias mappings, and role-skill requirements separately. |
| FR-03 | Stage unknown technical terms with frequency, lifecycle status, and an optional approved canonical mapping. |
| FR-04 | Track job-to-skill evidence to support reproducible local-demand calculations. |
| FR-05 | Store demand snapshots with job count, eligible-job denominator, score, and update time. |
| FR-06 | Represent candidate proficiency from 0 through 5 and retain the evidence source. |
| FR-07 | Use a minimum 70% assessment coverage gate before producing a ranked role list. |
| FR-08 | Sort ties by coverage, high-importance skill score, and alphabetical role title. |
| FR-09 | Calculate the technical gap using the documented role-importance and local-demand formula. |
| FR-10 | Return recommendation explanations grounded in stored evidence; identify unassessed skills separately from demonstrated gaps. |
| FR-11 | Support matching candidates to non-expired local vacancies. |
| FR-12 | Record sufficient timestamps and provenance to reproduce a recommendation from its source data. |

## Non-functional requirements

- **Privacy:** Minimize candidate data. Obtain informed consent before collecting
  resume or GitHub data; define retention, deletion, and access policies before
  enabling collection.
- **Security:** Validate inputs, restrict access to candidate profiles, protect
  secrets, and avoid storing raw credentials or access tokens in the database.
- **Data governance:** Preserve source, collection time, and extraction
  provenance. Respect data-source terms, rate limits, and applicable law.
- **Reliability:** Keep schema constraints for proficiency, demand ranges,
  relationship integrity, and candidate-review states.
- **Explainability:** Show source evidence and the factors contributing to a
  recommendation; do not present a model result as a guaranteed career outcome.
- **Maintainability:** Keep API, web UI, worker, ML, database, and documentation
  concerns separated.
- **Performance:** Index vector columns with pgvector HNSW and index common
  timestamp lookups. Confirm response-time targets after workload and hosting
  are agreed.
- **Accessibility:** Design later interfaces for keyboard navigation and
  readable contrast; validate against an agreed accessibility target.

## Acceptance criteria for the Phase 1 baseline

- The local database runs on PostgreSQL 16 with the pgvector extension
  available.
- The schema creates jobs, skills, aliases, candidate terms, roles, role-skill
  requirements, job-skill evidence, demand snapshots, candidate profiles, and
  candidate skills.
- Job and role embedding columns use the plan's 384 dimensions and have HNSW
  cosine indexes.
- Database constraints reject proficiency outside 0–5, required role level
  outside 1–5, invalid demand scores, invalid review status, and duplicate
  case-insensitive aliases.
- The draft seed contains exactly 44 technical skills and 19 roles, each role
  has at least one skill requirement, and every seeded skill is used by a role.
- The seed does not contain soft skills. Taxonomy names and mappings remain a
  draft pending local expert review.
- Initial market-demand scores are zero until vacancy evidence is loaded; no
  synthetic local-market statistics are presented as measured data.

## Assumptions and decisions requiring approval

1. The updated roadmap's Phase 1 is Weeks 1–3: architecture, schema, and
   baseline taxonomy. The next roadmap phase (Weeks 4–7) covers ingestion and
   dual extraction.
2. The supplied documents specify 44 skills and 19 roles but do not list their
   canonical names. The SQL seed is a proposed Sri Lankan IT-domain baseline,
   not a taxonomy transcribed from the documents.
3. A specific 384-dimensional Sentence-BERT model and vacancy sources have not
   been specified; select them after licensing, suitability, and evaluation
   review.
4. Resume storage, retention period, consent wording, authentication, counselor
   access, and the approved interpretation of a 0 proficiency score require
   stakeholder decisions before related features are built.
5. `W_type` is represented as the role-specific `importance_weight`; expert
   review must confirm the scale and how multiple roles' gaps are displayed.
6. Live demand is meaningful only if vacancy coverage, freshness, and
   collection permission are adequate. Display sample size and freshness with
   demand-driven outputs.
