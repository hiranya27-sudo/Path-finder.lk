import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from worker.career_worker.ingestion import (
    FixtureJobSource,
    load_fixture_jobs,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "worker" / "career_worker" / "fixtures" / "jobs.json"


class FixtureJobTests(unittest.TestCase):
    def test_fixture_jobs_are_valid_and_have_stable_source_ids(self) -> None:

        source = FixtureJobSource(FIXTURE_PATH)

        self.assertEqual(source.source_key, "fixture")
        self.assertTrue(source.is_fixture)
        self.assertTrue(source.fetch_jobs())

    def test_loader_rejects_duplicate_source_ids(self) -> None:
        fixture = [
            {"source_job_id": "duplicate", "title": "First", "description": "First"},
            {"source_job_id": "duplicate", "title": "Second", "description": "Second"},
        ]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "jobs.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Duplicate fixture source_job_id"):
                load_fixture_jobs(path)

    def test_loader_rejects_timestamps_without_timezone(self) -> None:
        fixture = [
            {
                "source_job_id": "naive-date",
                "title": "Posting",
                "description": "Description",
                "posted_at": "2026-01-05T00:00:00",
            }
        ]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "jobs.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "must include a timezone"):
                load_fixture_jobs(path)


if __name__ == "__main__":
    unittest.main()
