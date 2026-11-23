#!/usr/bin/env python3
"""hypopg-specific Windows regression tests kept with the extension.

The shared required-windows summary cases live in pgextwin/build
(tests/test-required-windows-summary.py) and run once in build's validate
CI. These cases cover this extension's own hooks and workflows and keep
running in this repo's Windows required summary job.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HypopgWindowsRegressionTests(unittest.TestCase):
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
        self.assertIn("ref: 3e5300afa99b99ea8c11be2a6ef75c994d708c28", probe)
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
        self.assertEqual(original.count('    - cron: "35 * * * *"'), 1)
        self.assertNotIn('    - cron: "41 * * * *"', original)
        self.assertEqual(original.count("    - cron:"), 1)
        self.assertIn("if: github.event_name == 'schedule'", original)
        self.assertNotIn("workflow_dispatch:", original)
        self.assertIn("needs: [authorize, watch_candidate]", original)
        self.assertIn("dry_run: false", original)
        self.assertIn(
            "operator-update-auto.yml@3e5300afa99b99ea8c11be2a6ef75c994d708c28",
            original)
        # The schedule-only callers use the protected central SHAs.
        self.assertIn(
            "check-extension-updates.yml@3e5300afa99b99ea8c11be2a6ef75c994d708c28",
            original)
        self.assertIn(
            "candidate-update.yml@3e5300afa99b99ea8c11be2a6ef75c994d708c28",
            original)
        self.assertNotIn(
            "operator-update-auto.yml@9ec4dde0b6defabc10cf3527c06cb69c13e5a7ff",
            original)
        self.assertIn("detector_sha: 3e5300afa99b99ea8c11be2a6ef75c994d708c28",
                      original)
        self.assertIn("candidate_attested_build:", original)
        self.assertIn("candidate_signed_audit:", original)
        self.assertNotIn("pull_request_target:", original)
    def test_native_candidate_audit_pin_has_independent_exact_pr_join(self):
        path = ROOT / ".github" / "workflows" / "update-watch.yml"
        contents = path.read_text(encoding="utf-8")
        self.assertIn(
            "verify-native-pr-candidate.yml@9ec4dde0b6defabc10cf3527c06cb69c13e5a7ff",
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
            "operator-update-auto.yml@3e5300afa99b99ea8c11be2a6ef75c994d708c28",
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
