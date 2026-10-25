#!/usr/bin/env python3
"""Test the exact stable aggregate check used by Windows CI, without Release."""
import importlib.util
from pathlib import Path
import os
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "summary", ROOT / "scripts" / "required_windows_summary.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class WindowsSummaryTests(unittest.TestCase):
    def test_success_only(self):
        self.assertTrue(module.verified_matrix_result("success"))
        for value in ("failure", "cancelled", "skipped", "", "Success",
                      "success ", True, 1, None):
            with self.subTest(value=value):
                self.assertFalse(module.verified_matrix_result(value))

    def test_real_exit_status_allow_and_deny(self):
        path = ROOT / "scripts" / "required_windows_summary.py"
        for value, expected in (("success", 0), ("failure", 2),
                                ("cancelled", 2), ("skipped", 2), ("", 2)):
            env = dict(os.environ, WINDOWS_MATRIX_RESULT=value)
            res = subprocess.run([sys.executable, str(path)], env=env,
                                 capture_output=True, text=True)
            with self.subTest(result=value):
                self.assertEqual(res.returncode, expected)

    def test_workflow_depends_on_complete_reusable_matrix_not_pg14_name(self):
        contents = (ROOT / ".github" / "workflows" / "windows.yml").read_text()
        self.assertIn("  windows_required:", contents)
        summary = contents.split("  windows_required:", 1)[1].split(
            "\n  candidate_report:", 1)[0]
        self.assertIn("name: Windows required summary", summary)
        self.assertIn("needs: windows", summary)
        self.assertIn("always()", summary)
        self.assertIn("needs.windows.result", summary)
        self.assertIn("scripts/required_windows_summary.py", summary)
        self.assertNotIn("PostgreSQL 14", summary)
        self.assertNotIn("workflow_dispatch:", summary)


    def test_on_demand_probe_cannot_authorize_signed_schedule(self):
        scheduled = (ROOT / ".github" / "workflows" / "update-watch.yml").read_text()
        probe = (ROOT / ".github" / "workflows" /
                 "on-demand-candidate-preflight.yml").read_text()
        self.assertIn("if: github.event_name == 'schedule'", scheduled)
        self.assertNotIn("workflow_dispatch:", scheduled)
        self.assertNotIn("on_demand_preflight:", scheduled)
        self.assertIn("  workflow_dispatch:", probe)
        self.assertIn('      - ".github/workflows/on-demand-candidate-preflight.yml"', probe)
        self.assertIn("github.event_name == 'workflow_dispatch'", probe)
        self.assertIn("github.event_name == 'push'", probe)
        self.assertIn("dry_run: true", probe)
        self.assertIn("ref: df9847fa265c06c8f8602a72cfb0fcde52ee46df", probe)
        self.assertIn("fleet-control.py", probe)
        self.assertIn("candidate-update.py plan", probe)
        self.assertIn("Reject central DENY", probe)
        self.assertIn("on-demand-candidate-plan-nonpublishing", probe)
        self.assertNotIn("candidate-update.yml@", probe)
        self.assertIn("contents: read", probe)
        for prohibited in ("contents: write", "pull-requests: write",
                           "id-token: write", "dry_run: false",
                           "publisher-candidate-intake.yml",
                           "build-extension-attested.yml"):
            self.assertNotIn(prohibited, probe)
        self.assertIn("needs: [authorize, watch_candidate]", scheduled)
        self.assertIn("dry_run: false", scheduled)
        self.assertNotIn("on-demand-candidate-preflight", scheduled)


if __name__ == "__main__":
    unittest.main()
