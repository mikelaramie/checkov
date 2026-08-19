from typing import Any, Dict, List

from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.terraform.checks.resource.base_resource_value_check import BaseResourceValueCheck

HARDWARE_PROTECTION_LEVELS = ("HSM", "HSM_SINGLE_TENANT")
SINGLE_TENANT_HSM_BACKEND = "singletenanthsminstances"


class GoogleKMSKeyHardwareBacked(BaseResourceValueCheck):
    def __init__(self) -> None:
        name = "Ensure KMS encryption keys are hardware-backed"
        id = "CKV_GCP_129"
        supported_resources = ("google_kms_crypto_key",)
        categories = (CheckCategories.ENCRYPTION,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf: Dict[str, List[Any]]) -> CheckResult:
        backend = conf.get("crypto_key_backend")
        if backend:
            backend_value = backend[0] if isinstance(backend, list) else backend
            if self._is_variable_dependant(backend_value):
                return CheckResult.UNKNOWN
            if isinstance(backend_value, str) and SINGLE_TENANT_HSM_BACKEND in backend_value.lower():
                self.evaluated_keys = ["crypto_key_backend"]
                return CheckResult.PASSED
        return super().scan_resource_conf(conf)

    def get_inspected_key(self) -> str:
        return "version_template/[0]/protection_level"

    def get_expected_value(self) -> str:
        return "HSM"

    def get_expected_values(self) -> List[Any]:
        return list(HARDWARE_PROTECTION_LEVELS)


check = GoogleKMSKeyHardwareBacked()
