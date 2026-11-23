# Tests and evaluation

Phase 1 acceptance criteria are listed in
[`../docs/phase-1/requirements-and-scope.md`](../docs/phase-1/requirements-and-scope.md).

From the project root, run the dependency-free draft taxonomy checks:

```powershell
python -m unittest discover -s tests -v
```

Add database integration tests when a local PostgreSQL 16 + pgvector instance
is available. The final-project ranking evaluation is planned against
10–15 expert reference personas using Precision@K, Recall@K, and NDCG@K.
