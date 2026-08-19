import os
import unittest

from checkov.runner_filter import RunnerFilter
from checkov.terraform.checks.resource.gcp.GoogleKMSKeyHardwareBacked import check
from checkov.terraform.runner import Runner


class TestGoogleKMSKeyHardwareBacked(unittest.TestCase):
    def test(self):
        runner = Runner()
        current_dir = os.path.dirname(os.path.realpath(__file__))

        test_files_dir = current_dir + "/example_GoogleKMSKeyHardwareBacked"
        report = runner.run(root_folder=test_files_dir, runner_filter=RunnerFilter(checks=[check.id]))
        summary = report.get_summary()

        passing_resources = {
            "google_kms_crypto_key.pass_hsm",
            "google_kms_crypto_key.pass_hsm_single_tenant",
            "google_kms_crypto_key.pass_single_tenant_backend",
        }
        failing_resources = {
            "google_kms_crypto_key.fail_default",
            "google_kms_crypto_key.fail_software",
            "google_kms_crypto_key.fail_omit_protection_level",
            "google_kms_crypto_key.fail_external",
            "google_kms_crypto_key.fail_external_vpc",
        }

        passed_check_resources = {c.resource for c in report.passed_checks}
        failed_check_resources = {c.resource for c in report.failed_checks}

        self.assertEqual(summary["passed"], len(passing_resources))
        self.assertEqual(summary["failed"], len(failing_resources))
        self.assertEqual(summary["skipped"], 0)
        self.assertEqual(summary["parsing_errors"], 0)

        self.assertEqual(passing_resources, passed_check_resources)
        self.assertEqual(failing_resources, failed_check_resources)


if __name__ == "__main__":
    unittest.main()
