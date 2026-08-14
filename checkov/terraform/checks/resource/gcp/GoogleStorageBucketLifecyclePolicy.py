from __future__ import annotations

from typing import Any

from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.common.util.type_forcers import force_int
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

MIN_RETENTION_DAYS = 90
ARCHIVE_AFTER_DAYS = 180
ARCHIVAL_STORAGE_CLASSES = {"ARCHIVE"}


class GoogleStorageBucketLifecyclePolicy(BaseResourceCheck):
    def __init__(self) -> None:
        name = (
            "Ensure Cloud Storage buckets have a lifecycle policy that retains data "
            "for at least 90 days and moves it to Archive storage after 180 days"
        )
        id = "CKV_GCP_128"
        supported_resources = ("google_storage_bucket",)
        categories = (CheckCategories.BACKUP_AND_RECOVERY,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf: dict[str, list[Any]]) -> CheckResult:
        self.evaluated_keys = ["lifecycle_rule"]
        rules = conf.get("lifecycle_rule")
        if not rules or not isinstance(rules, list):
            return CheckResult.FAILED

        saw_unresolved_age = False
        has_archive_rule = False
        for idx, rule in enumerate(rules):
            if not isinstance(rule, dict):
                continue
            action = _first(rule.get("action"))
            condition = _first(rule.get("condition"))
            if not isinstance(action, dict):
                continue

            action_type = _first(action.get("type"))
            age = _age_in_days(condition)

            if age is _UNRESOLVED:
                saw_unresolved_age = True
                continue

            if action_type == "Delete" and (age is None or age < MIN_RETENTION_DAYS):
                self.evaluated_keys = [f"lifecycle_rule/[{idx}]/condition/[0]/age"]
                return CheckResult.FAILED

            if action_type == "SetStorageClass" and age is not None and age >= ARCHIVE_AFTER_DAYS:
                storage_class = _first(action.get("storage_class"))
                if isinstance(storage_class, str) and storage_class.upper() in ARCHIVAL_STORAGE_CLASSES:
                    self.evaluated_keys = [
                        f"lifecycle_rule/[{idx}]/action/[0]/type",
                        f"lifecycle_rule/[{idx}]/action/[0]/storage_class",
                        f"lifecycle_rule/[{idx}]/condition/[0]/age",
                    ]
                    has_archive_rule = True

        if has_archive_rule:
            return CheckResult.PASSED
        if saw_unresolved_age:
            return CheckResult.UNKNOWN
        return CheckResult.FAILED


_UNRESOLVED = object()


def _first(value: Any) -> Any:
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _age_in_days(condition: Any) -> int | None | object:
    if not isinstance(condition, dict):
        return None
    raw = _first(condition.get("age"))
    if raw is None:
        return None
    age = force_int(raw)
    if age is None:
        return _UNRESOLVED
    return age


check = GoogleStorageBucketLifecyclePolicy()
