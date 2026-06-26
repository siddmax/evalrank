import json
import re
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

    def test_python_package_readmes_match_manifest_metadata(self):
        imports = {
            "core": "evalrank_core",
            "sdk-python": "evalrank_sdk",
            "cli": "evalrank_cli",
            "mcp": "evalrank_mcp",
        }

        for package, import_name in imports.items():
            with self.subTest(package=package):
                project = _pyproject(package)["project"]
                readme = (PACKAGES / package / "README.md").read_text(encoding="utf-8")

                self.assertIn(f"`{project['name']}`", readme)
                self.assertIn(f"`{import_name}`", readme)
                self.assertIn(f"`{project['license']}`", readme)
                for dependency in project.get("dependencies", []):
                    self.assertIn(f"`{dependency}`", readme)
                for script in project.get("scripts", {}):
                    self.assertIn(f"`{script}`", readme)
                expected_metadata = {
                    "Distribution": {project["name"]},
                    "Import": {import_name},
                    "License": {project["license"]},
                }
                dependencies = set(project.get("dependencies", []))
                if dependencies:
                    label = "Runtime dependency" if len(dependencies) == 1 else "Runtime dependencies"
                    expected_metadata[label] = dependencies
                if project.get("scripts"):
                    expected_metadata["Entrypoint"] = set(project["scripts"])
                self.assertEqual(expected_metadata, _readme_metadata(package))

    def test_typescript_package_readme_matches_manifest_metadata(self):
        package = json.loads((PACKAGES / "sdk-ts" / "package.json").read_text(encoding="utf-8"))
        readme = (PACKAGES / "sdk-ts" / "README.md").read_text(encoding="utf-8")

        self.assertIn(f"`{package['name']}`", readme)
        self.assertIn(f"`{package['type']}`", readme)
        self.assertIn(f"`{package['types']}`", readme)
        self.assertIn(f"`{package['license']}`", readme)
        self.assertIn("`private`", readme)
        self.assertEqual(
            {
                "Package": {package["name"]},
                "Type": {package["type"]},
                "Types": {package["types"]},
                "License": {package["license"]},
                "Publish status": {"private"},
            },
            _readme_metadata("sdk-ts"),
        )


def _pyproject(package: str) -> dict:
    with (PACKAGES / package / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)


def _readme_metadata(package: str) -> dict[str, set[str]]:
    lines = (PACKAGES / package / "README.md").read_text(encoding="utf-8").splitlines()
    start = lines.index("Package metadata:") + 1
    metadata: dict[str, set[str]] = {}
    for line in lines[start:]:
        if not line.strip() and metadata:
            break
        match = re.fullmatch(r"- ([^:]+): (.+)", line)
        if match:
            metadata[match.group(1)] = set(re.findall(r"`([^`]+)`", match.group(2)))
    return metadata


if __name__ == "__main__":
    unittest.main()
