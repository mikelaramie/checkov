# Test layout

Parse real Terraform through `Runner`. Assert **resource ID sets**, not only pass/fail counts. Do not build `conf` dicts by hand.

## Python resource check

```
tests/terraform/checks/resource/<provider>/
  example_<ClassName>/
    main.tf          # pass and fail resources
  test_<ClassName>.py
```

Canonical pattern: `tests/terraform/checks/resource/aws/test_IAMAdminPolicyDocument.py`.

- `Runner().run(root_folder=..., runner_filter=RunnerFilter(checks=[check.id]))`
- Compare `report.passed_checks` / `failed_checks` resource names to expected sets
- Also assert `summary['skipped'] == 0` and `summary['parsing_errors'] == 0`

Run: `pytest -k test_<ClassName>`

## YAML graph check

```
tests/terraform/graph/checks/resources/<PolicyName>/
  main.tf
  expected.yaml      # pass: / fail: lists of resource addresses
```

Add to `tests/terraform/graph/checks/test_yaml_policies.py`:

```python
def test_<PolicyName>(self):
    self.go("<PolicyName>")
```

`PolicyName` must match the YAML filename (without `.yaml`) and the resources folder name.

`expected.yaml` example:

```yaml
pass:
  - "google_compute_network.pass"
fail:
  - "google_compute_network.fail"
```

Run: `pytest -k test_<PolicyName>`
