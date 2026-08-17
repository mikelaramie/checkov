# Test layout

Follow root [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) “Tests for new checks” and [../contributing.md](../contributing.md).

Parse real Terraform through `Runner`. Assert **resource ID sets**, not only pass/fail counts. Do not build `conf` dicts by hand (CONTRIBUTING rejects that pattern; see `test_ALBListenerHTTPS.py`).

## Python resource check

```
tests/terraform/checks/resource/<provider>/
  example_<ClassName>/
    main.tf          # pass and fail resources
  test_<ClassName>.py
```

Canonical pattern (named in CONTRIBUTING): `tests/terraform/checks/resource/aws/test_IAMAdminPolicyDocument.py`.

- `Runner().run(root_folder=..., runner_filter=RunnerFilter(checks=[check.id]))`
- Compare `report.passed_checks` / `failed_checks` resource names to expected sets
- Also assert `summary['skipped'] == 0` and `summary['parsing_errors'] == 0`
- CONTRIBUTING allows string templates if runner-parsed; prefer files for reviewability

Preferred run (CONTRIBUTING):

```bash
pipenv run pytest -k test_<ClassName>
```

Fallback: `pytest -k test_<ClassName> -o addopts=` in `.venv`.

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

Run: `pipenv run pytest -k test_<PolicyName>` (or fallback as above).
