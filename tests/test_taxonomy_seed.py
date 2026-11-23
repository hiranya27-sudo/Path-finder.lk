import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "database" / "seeds" / "001_initial_taxonomy.sql"


def _insert_values_block(sql: str, table: str) -> str:
    match = re.search(
        rf"INSERT INTO {table}\b.*?VALUES\s*(.*?)\nON CONFLICT",
        sql,
        re.DOTALL | re.IGNORECASE,
    )
    if match is None:
        raise AssertionError(f"Could not find INSERT values for {table}")
    return match.group(1)


def _catalog_names(sql: str, table: str) -> set[str]:
    block = _insert_values_block(sql, table)
    return {
        match.group(1)
        for match in re.finditer(r"\('((?:''|[^'])*)',\s*'[^']+'\)", block)
    }


class TaxonomySeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.seed_sql = SEED_PATH.read_text(encoding="utf-8")
        mapping_match = re.search(
            r"INSERT INTO role_skills\b.*?VALUES\s*(.*?)\n\) AS mapping",
            cls.seed_sql,
            re.DOTALL,
        )
        if mapping_match is None:
            raise AssertionError("Could not find role-skill mapping values")
        cls.mappings = re.findall(
            r"\('((?:''|[^'])*)',\s*'((?:''|[^'])*)',\s*\d+,\s*[\d.]+\)",
            mapping_match.group(1),
        )

    def test_seed_has_expected_catalog_sizes(self) -> None:
        self.assertEqual(len(_catalog_names(self.seed_sql, "job_roles")), 19)
        self.assertEqual(len(_catalog_names(self.seed_sql, "skills")), 44)

    def test_every_seeded_role_and_skill_has_a_requirement_mapping(self) -> None:
        roles = _catalog_names(self.seed_sql, "job_roles")
        skills = _catalog_names(self.seed_sql, "skills")
        mapped_roles = {role for role, _ in self.mappings}
        mapped_skills = {skill for _, skill in self.mappings}

        self.assertEqual(mapped_roles, roles)
        self.assertEqual(mapped_skills, skills)


if __name__ == "__main__":
    unittest.main()
