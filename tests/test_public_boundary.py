import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPO_ROOT / "scripts" / "check_public_boundary.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_public_boundary", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class PublicBoundaryTests(unittest.TestCase):
    def test_rejects_private_imports_and_disallowed_methods(self):
        checker = load_checker()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "LICENSE", "Apache-2.0\n")
            write(root / "NOTICE", "EvalRank\n")
            write(root / "packages/core/LICENSE", "Apache-2.0\n")
            write(root / "packages/core/NOTICE", "EvalRank core\n")
            write(
                root / "packages/core/src/evalrank_core/ranker.py",
                """
                import syndai.backend.internal
                from smithery import Client
                from evalrank_core.methods.min_k_percent import score
                """,
            )

            violations = list(checker.check_repository(root))
            codes = {violation.code for violation in violations}

        self.assertIn("private-import", codes)
        self.assertIn("smithery-import", codes)
        self.assertIn("min-k-percent", codes)

    def test_rejects_public_packages_without_license_and_notice(self):
        checker = load_checker()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "LICENSE", "Apache-2.0\n")
            write(root / "NOTICE", "EvalRank\n")
            write(root / "packages/core/src/evalrank_core/__init__.py", "__version__ = '0.0.0'\n")

            violations = list(checker.check_repository(root))
            codes = {violation.code for violation in violations}

        self.assertIn("missing-package-license", codes)
        self.assertIn("missing-package-notice", codes)

    def test_accepts_clean_public_scaffold(self):
        checker = load_checker()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "LICENSE", "Apache-2.0\n")
            write(root / "NOTICE", "EvalRank\n")
            write(root / "packages/core/LICENSE", "Apache-2.0\n")
            write(root / "packages/core/NOTICE", "EvalRank core\n")
            write(root / "packages/core/src/evalrank_core/__init__.py", "__version__ = '0.0.0'\n")
            write(root / "packages/mcp/LICENSE", "Apache-2.0\n")
            write(root / "packages/mcp/NOTICE", "EvalRank MCP\n")
            write(root / "packages/mcp/src/evalrank_mcp/__init__.py", "")

            violations = list(checker.check_repository(root))

        self.assertEqual([], violations)

    def test_cli_reports_violations_and_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "LICENSE", "Apache-2.0\n")
            write(root / "NOTICE", "EvalRank\n")
            write(root / "packages/core/src/evalrank_core/leak.py", "from syndai.secret import token\n")

            result = subprocess.run(
                [sys.executable, str(CHECKER_PATH), "--root", str(root)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        self.assertEqual(1, result.returncode)
        self.assertIn("private-import", result.stdout)
        self.assertIn("packages/core/src/evalrank_core/leak.py", result.stdout)

    def test_rejects_secret_files_private_data_paths_and_secret_values(self):
        checker = load_checker()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "LICENSE", "Apache-2.0\n")
            write(root / "NOTICE", "EvalRank\n")
            write(root / ".env", "DATABASE_URL=postgres://example.invalid/evalrank\n")
            write(root / ".env.staging", "DATABASE_URL=postgres://example.invalid/evalrank\n")
            write(root / ".env.example", "DATABASE_URL=postgres://example.invalid/evalrank\n")
            write(root / "private.pem", "not a real key\n")
            write(root / "tests/fixtures/held-out/cases.json", "[]\n")
            fake_secret = "sk-" + ("a" * 48)
            write(root / "README.md", f"OPENAI_API_KEY={fake_secret}\n")
            write(root / "Makefile", f"check:\n\tOPENAI_API_KEY={fake_secret} python3 -m unittest\n")

            violations = list(checker.check_repository(root))
            codes = {violation.code for violation in violations}

        self.assertIn("secret-file", codes)
        self.assertIn("private-data-path", codes)
        self.assertIn("secret-value", codes)

    def test_accepts_public_env_example_without_secret_values(self):
        checker = load_checker()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "LICENSE", "Apache-2.0\n")
            write(root / "NOTICE", "EvalRank\n")
            write(root / ".env.example", "DATABASE_URL=postgres://example.invalid/evalrank\n")

            violations = list(checker.check_repository(root))

        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
