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
        self.assertNotIn("candidate-update.py propose", probe)
        self.assertNotIn("name: candidate-decision", probe)
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


    def test_offpeak_candidate_schedule_keeps_exact_schedule_only_gate(self):
        original = (ROOT / ".github" / "workflows" / "update-watch.yml").read_text()
        self.assertEqual(original.count('    - cron: "30 * * * *"'), 1)
        self.assertEqual(original.count('    - cron: "41 * * * *"'), 1)
        self.assertEqual(original.count("    - cron:"), 2)
        self.assertIn("if: github.event_name == 'schedule'", original)
        self.assertNotIn("workflow_dispatch:", original)
        self.assertIn("needs: [authorize, watch_candidate]", original)
        self.assertIn("dry_run: false", original)
        self.assertIn(
            "operator-update-auto.yml@bf5ce09746f4ff6cf439ac1571a9c2646983fdcc",
            original)
        self.assertIn("detector_sha: 16b886b9d06d6f389b369b87ce0c155767697ca0",
                      original)
        self.assertIn("candidate_attested_build:", original)
        self.assertIn("candidate_signed_audit:", original)
        self.assertNotIn("pull_request_target:", original)

    def test_native_candidate_audit_pin_has_independent_exact_pr_join(self):
        path = ROOT / ".github" / "workflows" / "update-watch.yml"
        contents = path.read_text(encoding="utf-8")
        self.assertIn(
            "verify-native-pr-candidate.yml@bf5ce09746f4ff6cf439ac1571a9c2646983fdcc",
            contents)
        self.assertNotIn(
            "verify-native-pr-candidate.yml@2b2903e463d28891b5688bf4546da99a299c3684",
            contents)
        self.assertIn("github.event.workflow_run.event == 'pull_request'", contents)
        self.assertIn("github.event.workflow_run.conclusion == 'success'", contents)
        self.assertIn("startsWith(github.event.workflow_run.head_branch, 'auto-candidate/')",
                      contents)
        self.assertIn("if: github.event_name == 'schedule'", contents)
        self.assertIn("candidate_main_merge_observation:", contents)
        self.assertIn("candidate_attested_build:", contents)
        self.assertIn("candidate_signed_audit:", contents)
        self.assertIn(
            "operator-update-auto.yml@bf5ce09746f4ff6cf439ac1571a9c2646983fdcc",
            contents)

    def test_version_independent_windows_pipeline(self):
        scripts = ROOT / "windows" / "ci"
        source = {name: (scripts / name).read_text(encoding="utf-8")
                  for name in ("build.ps1", "install.ps1",
                               "package.ps1", "smoke-test.ps1")}
        for name, body in source.items():
            with self.subTest(file=name):
                self.assertNotIn("1.4.3", body)
                self.assertIn("config/extension.json", body)
                self.assertIn("upstream.version", body)
        self.assertIn("upstream.commit", source["build.ps1"])
        self.assertIn("[regex]::Escape($expectedVersion)", source["build.ps1"])
        self.assertIn("[regex]::Escape($expectedVersion)", source["install.ps1"])
        self.assertIn("[regex]::Escape($UpstreamVersion)", source["package.ps1"])
        self.assertIn('hypopg--$expectedVersion.sql', source["install.ps1"])
        self.assertIn('hypopg--$UpstreamVersion.sql', source["package.ps1"])
        self.assertIn("sqlBody.Replace('@@EXPECTED_HYPOPG_VERSION@@', $expectedVersion)",
                      source["smoke-test.ps1"])
        for name in ("build.ps1", "install.ps1", "smoke-test.ps1"):
            self.assertIn("'^[0-9]+\\.[0-9]+\\.[0-9]+$'", source[name])


if __name__ == "__main__":
    unittest.main()
