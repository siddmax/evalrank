import re
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [Path(line) for line in result.stdout.splitlines()]


class RepoDocsTests(unittest.TestCase):
    def test_claude_md_is_agents_shim(self):
        text = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")

        self.assertEqual("@AGENTS.md\n", text)

    def test_repo_structure_tracks_public_top_level_directories(self):
        text = (REPO_ROOT / "docs" / "REPO_STRUCTURE.md").read_text(encoding="utf-8")
        top_level_dirs = {path.parts[0] for path in tracked_paths() if len(path.parts) > 1}
        expected_refs = {
            ".github": ".github/workflows/",
            "docs": "docs/",
            "examples": "examples/",
            "methods": "methods/",
            "packages": "packages/",
            "schemas": "schemas/",
            "scripts": "scripts/",
            "tests": "tests/",
        }

        self.assertEqual(set(expected_refs), top_level_dirs)
        missing_refs = {
            directory: ref
            for directory, ref in expected_refs.items()
            if f"`{ref}`" not in text
        }
        self.assertEqual({}, missing_refs)

    def test_repo_structure_lists_package_directories_exactly(self):
        text = (REPO_ROOT / "docs" / "REPO_STRUCTURE.md").read_text(encoding="utf-8")
        documented = set(re.findall(r"`packages/([^`/]+)/`", text))
        expected = {
            path.parts[1]
            for path in tracked_paths()
            if len(path.parts) > 2 and path.parts[0] == "packages"
        }

        self.assertEqual(expected, documented)


if __name__ == "__main__":
    unittest.main()
