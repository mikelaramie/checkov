# Check and test anti-patterns

Source of truth: root [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) “Tests for new checks” and [../contributing.md](../contributing.md).

## Tests (critical)

| Bad | Good |
|-----|------|
| `resource_conf = {'encryption': [{'…': True}]}` then `check.scan_resource_conf(resource_conf)` | `Runner().run(root_folder=example_dir, runner_filter=RunnerFilter(checks=[check.id]))` |
| `self.assertEqual(summary['failed'], 2)` only | Also `self.assertEqual(failing_resources, failed_check_resources)` |
| Only happy-path Terraform | At least one fail resource that violates the policy |
| Inline giant HCL string with no file | Prefer `example_<ClassName>/main.tf` (string OK if still runner-parsed — CONTRIBUTING allows string templates) |

CONTRIBUTING explicitly rejects hard-coded conf objects (example called out: `test_ALBListenerHTTPS.py`) and requires listing which resources pass/fail. Canonical good style: `test_IAMAdminPolicyDocument.py`. **Do not copy** legacy hand-built conf tests such as `test_DynamodbRecovery.py`.

## Python checks

| Bad | Good |
|-----|------|
| Inspecting `conf["foo"]["bar"]` without list unwrap | Paths like `encryption/[0]/kms_key_name` via value-check helpers |
| Custom `BaseResourceCheck` for a single boolean | `BaseResourceValueCheck` / `BaseResourceNegativeValueCheck` |
| Policy needs `google_x` connected to `google_y` | YAML graph check (`CKV2_*`) |
| Filling `CKV_GCP_5` because the number is free | Next free = max + 1 |
| Raw `re.match(...)` patterns scattered without compile | `re.compile` (CONTRIBUTING / flake8) |

## YAML graph checks

| Bad | Good |
|-----|------|
| Filename / folder / `self.go("…")` names disagree | Same `PolicyName` everywhere |
| No `expected.yaml` | `pass:` / `fail:` resource addresses |
| Using graph for one attribute on one type when Python is clearer | Prefer Python value check unless connection/AND-OR needs graph |

## Review comment tone

Link `CONTRIBUTING.md` and the canonical test file. Prefer "replace hand-built conf with runner fixtures per CONTRIBUTING" over "this is wrong."
