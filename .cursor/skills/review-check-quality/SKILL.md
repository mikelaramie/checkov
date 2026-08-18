---
name: review-check-quality
description: Reviews a new or changed Checkov check and its tests against CONTRIBUTING.md standards—runner-parsed fixtures, resource ID assertions, anti-patterns, and review readiness. Use when the user asks to review a check, strengthen tests, catch mistakes before review, QA a check PR, or run a pre-review pass on CKV / CKV2 changes.
---

# Review check quality

Run this **before** asking for human review or opening a PR. Enforce [contributing.md](../contributing.md) / root `CONTRIBUTING.md` “Tests for new checks.” Fix critical findings when the user wants them fixed; otherwise report only.

## SDLC

- Phase: review (targeted test in step 5)
- Must not: claim CI-ready or open a PR; skip CONTRIBUTING test-standard blockers
- Next: `prepare-ci-ready-pr` (`Make this PR CI-ready`) when verdict is Ready for review; optionally `qa-fixture-review` for fixture coverage
- Source of truth: CONTRIBUTING.md — Tests for new checks

## Workflow

```
- [ ] 1. Identify the change set
- [ ] 2. Check layout and ID
- [ ] 3. Check implementation anti-patterns
- [ ] 4. Check tests and fixtures (CONTRIBUTING)
- [ ] 5. Run targeted tests (prefer pipenv)
- [ ] 6. Report findings (severity + file:line)
```

### 1. Identify the change set

From git status / diff or paths the user names, list:

- Check file(s) under `checkov/terraform/checks/`
- Test file(s) and `example_*` / graph `resources/` fixtures

If nothing looks like a check change, say so and stop (point to `prepare-ci-ready-pr` for non-check PRs).

### 2. Layout and ID

- Python: `checkov/terraform/checks/resource|data|provider/<provider>/`
- YAML graph: `checkov/terraform/checks/graph_checks/<provider>/`
- ID prefix matches type: `CKV_` (Python) vs `CKV2_` (YAML)
- ID is **max existing + 1** for that prefix; do not fill retired gaps (GCP Python skips `_5`, `_19`, `_67`)
- Module ends with `check = ClassName()` for Python
- Check `name` is a positive outcome ("Ensure …")
- Regex uses `re.compile` (CONTRIBUTING)

### 3. Implementation anti-patterns

Read [anti-patterns.md](anti-patterns.md). Flag:

- Hand-tuned logic that ignores Terraform list-wrapping (`attr/[0]/…`)
- Wrong base class for a simple equals/not-equals case
- Graph-shaped policy written as brittle Python (or the reverse)
- Missing `supported_resources` / `metadata.category`
- Copy-paste from an unrelated provider without adjusting keys

### 4. Tests and fixtures

CONTRIBUTING standard (cite in review comments):

- Good: `tests/terraform/checks/resource/aws/test_IAMAdminPolicyDocument.py`
- Bad (do not copy): `tests/terraform/checks/resource/aws/test_ALBListenerHTTPS.py`

**Must fail the review if:**

- Test builds `conf` / `resource_conf` dicts by hand and calls `check.scan_resource_conf` (explicitly rejected in CONTRIBUTING)
- Only asserts pass/fail **counts**, not **resource ID sets** (CONTRIBUTING)
- Missing at least one pass and one fail fixture
- Fixtures not parsed through `Runner` + `RunnerFilter(checks=[check.id])`
- Graph check missing `expected.yaml` or `test_*` / `self.go("PolicyName")` wiring

**Should strengthen if:**

- Resource names are opaque (`bucket1`) instead of `pass` / `fail` / `pass_archive`
- Edge cases from the requirement (exceptions, thresholds) have no fixture
- `summary['skipped']` / `parsing_errors` not asserted
- No issue linked / no `fast-lane` plan for a new check PR

### 5. Run tests

Preferred:

```bash
pipenv run pytest -k test_<Name>
```

Fallback: project `.venv` + `pytest -k test_<Name> -o addopts=`. Note environment issues separately from check bugs.

### 6. Report

Use:

- **Critical** — must fix before review (CONTRIBUTING violations, wrong ID, hand-built conf, no fail fixture, test fails)
- **Should fix** — weak coverage, naming, missing edge case, missing docs note
- **Nit** — style only

End with a one-line verdict: **Ready for review** or **Not ready** (list blockers). Point next step to `prepare-ci-ready-pr` (pre-commit, PR etiquette, `fast-lane`).

## Who uses this

- Engineers: after `add-terraform-check`, before PR
- QA: same checklist on an open PR or branch (`gh pr diff` / local checkout)
