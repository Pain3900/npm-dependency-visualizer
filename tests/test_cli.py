"""Проверки параметров через командную строку."""

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    """Запустить CLI из корня проекта."""
    return subprocess.run(
        [sys.executable, "src/main.py", *args],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )


class CliTests(unittest.TestCase):
    def test_bad_arguments(self):
        cases = [
            (["--package", "!!", "--repo", "https://example.org"], "--package"),
            (["--package", "abc", "--repo", "oops"], "--repo"),
            (["--package", "A", "--repo", "absent.json", "--test"], "--repo"),
            (["--test=yes"], "--test"),
            (["--ascii=yes"], "--ascii"),
            (["--package", "abc", "--repo", "https://x", "--filter", ""],
             "--filter"),
        ]
        for args, option in cases:
            with self.subTest(args=args):
                result = run_cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertIn(option, result.stderr)
