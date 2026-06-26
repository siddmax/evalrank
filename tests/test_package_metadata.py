import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGES = REPO_ROOT / "packages"


EXPECTED_PROJECTS = {
    "core": {
        "name": "evalrank-core",
        "description": "Public EvalRank core contracts",
        "dependencies": [],
    },
    "sdk-python": {
        "name": "evalrank-sdk",
        "description": "Public EvalRank Python SDK",
        "dependencies": ["evalrank-core==0.0.0"],
    },
    "cli": {
        "name": "evalrank-cli",
        "description": "Public EvalRank CLI",
        "dependencies": ["evalrank-core==0.0.0", "evalrank-sdk==0.0.0"],
        "scripts": {"evalrank": "evalrank_cli:main"},
    },
    "mcp": {
        "name": "evalrank-mcp",
        "description": "Public EvalRank MCP adapter",
        "dependencies": ["evalrank-core==0.0.0", "evalrank-sdk==0.0.0"],
    },
}


class PackageMetadataTests(unittest.TestCase):
    def test_python_package_metadata_is_public_and_pinned(self):
        self.assertEqual(set(EXPECTED_PROJECTS), {path.parent.name for path in PACKAGES.glob("*/pyproject.toml")})

        for package, expected in EXPECTED_PROJECTS.items():
            with self.subTest(package=package):
                project = _pyproject(package)["project"]
                self.assertEqual(expected["name"], project["name"])
                self.assertEqual("0.0.0", project["version"])
                self.assertEqual(expected["description"], project["description"])
                self.assertEqual(">=3.11", project["requires-python"])
                self.assertEqual("Apache-2.0", project["license"])
                self.assertEqual(expected["dependencies"], project.get("dependencies", []))

    def test_cli_entrypoint_stays_public_and_scriptable(self):
        scripts = _pyproject("cli")["project"]["scripts"]

        self.assertEqual({"evalrank": "evalrank_cli:main"}, scripts)

    def test_tests_doc_lists_package_metadata_guard(self):
        tests_doc = (REPO_ROOT / "TESTS.md").read_text(encoding="utf-8")

        self.assertIn("tests/test_package_metadata.py", tests_doc)


def _pyproject(package: str) -> dict:
    with (PACKAGES / package / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)


if __name__ == "__main__":
    unittest.main()
