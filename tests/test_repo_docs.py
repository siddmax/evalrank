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

    def test_scoped_agents_cover_public_work_areas(self):
        package_dirs = {
            f"packages/{path.parts[1]}"
            for path in tracked_paths()
            if len(path.parts) > 2 and path.parts[0] == "packages"
        }
        scoped_dirs = {
            "docs",
            "examples",
            "methods",
            "packages",
            "schemas",
            "scripts",
            "tests",
            *package_dirs,
        }
        missing = sorted(
            directory
            for directory in scoped_dirs
            if not (REPO_ROOT / directory / "AGENTS.md").is_file()
        )

        self.assertEqual([], missing)

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

    def test_status_lists_build_logs_exactly(self):
        text = (REPO_ROOT / "docs" / "STATUS.md").read_text(encoding="utf-8")
        documented = set(re.findall(r"`(docs/build-log/[^`]+\.md)`", text))
        expected = {
            str(path.relative_to(REPO_ROOT))
            for path in (REPO_ROOT / "docs" / "build-log").glob("*.md")
        }

        self.assertEqual(expected, documented)

    def test_status_mentions_current_porting_workstreams(self):
        status_text = (REPO_ROOT / "docs" / "STATUS.md").read_text(encoding="utf-8")
        porting_text = (REPO_ROOT / "docs" / "PORTING.md").read_text(encoding="utf-8")
        match = re.search(
            r"## Current Workstreams\n\n(?P<body>.*?)(?:\n## |\Z)",
            porting_text,
            re.S,
        )
        self.assertIsNotNone(match)
        workstreams = [
            item.strip()
            for item in re.findall(r"^- ([^:\n]+):", match.group("body"), re.M)
        ]
        missing = [
            workstream for workstream in workstreams if workstream not in status_text
        ]

        self.assertNotEqual([], workstreams)
        self.assertEqual([], missing)

    def test_public_mcp_docs_do_not_advertise_private_evidence_lookup(self):
        checked_paths = (
            "README.md",
            "packages/mcp/AGENTS.md",
            "packages/mcp/README.md",
        )
        forbidden_phrases = (
            "evidence lookup tools",
            "evidence and evaluation tools",
        )
        offenders = []
        for relative_path in checked_paths:
            text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    offenders.append(f"{relative_path}: {phrase}")

        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
