---
name: qa-fixture-review
description: Reviews Checkov check pass/fail fixtures against CONTRIBUTING.md test standards (runner parsing, resource ID assertions) and requirement coverage. Use when QA reviews a check, asks whether fixtures are enough, strengthens tests, writes a test plan for a CKV policy, or validates example Terraform before merge.
---

# QA fixture review

Focus on **whether the tests prove the policy** per [contributing.md](../contributing.md) / root `CONTRIBUTING.md`. Use `review-check-quality` for code structure anti-patterns.

## Workflow

```
- [ ] 1. Load requirement and change
- [ ] 2. Map requirement → expected cases
- [ ] 3. Diff fixtures vs that map
- [ ] 4. Check assertions (CONTRIBUTING)
- [ ] 5. Produce QA verdict + optional test plan comment
```

### 1. Load requirement and change

- Issue body (GRC form fields if present) — CONTRIBUTING expects detailed description + examples
- PR or branch: check file + `example_*` / graph `resources/` + test module
- PR **Assumptions / GRC clarifications** if present

### 2. Expected cases

From the requirement, list cases that should exist:

| Case | Example |
|------|---------|
| Happy path | Meets threshold / has required block |
| Clear violation | Missing policy, wrong value |
| Boundary | Exactly 90 days vs 89 |
| Exception | Label/`retention:none` if in scope |
| Non-target | Wrong resource type not in fail set |

Mark each **required for merge** vs **nice follow-up**.

### 3. Diff fixtures

For each required case, point to a resource in `main.tf` / `expected.yaml` or mark **MISSING**.

Flag opaque names (`bucket1`) that make QA/review harder; suggest `pass_*` / `fail_*`.

### 4. Assertions

CONTRIBUTING “Tests for new checks” — **block** if violated:

- Templates/files parsed through the **runner** (not hand-built `conf` objects; bad pattern: `test_ALBListenerHTTPS.py`)
- Test **explicitly lists** which resources pass and which fail (counts alone are not enough)
- Canonical good pattern: `test_IAMAdminPolicyDocument.py`
- Prefer also asserting `skipped == 0` and `parsing_errors == 0`

String templates are allowed by CONTRIBUTING if still runner-parsed; file-based `example_*` fixtures are preferred for reviewability.

### 5. Verdict

```markdown
## QA fixture review

**Verdict:** Pass | Pass with follow-ups | Block

**CONTRIBUTING test standard:** Met | Not met (explain)

**Coverage**
- [x] …
- [ ] MISSING: …

**Assertions:** OK | Weak (explain)

**Recommended issue comment / PR comment:**
…
```

If the user wants it on GitHub:

```bash
gh pr comment <n> --body "…"
# or
gh issue comment <n> --body "…"
```

Do not rewrite production check logic unless asked; prefer listing missing fixtures for eng. Mention `fast-lane` only if the PR is a new check and the label is missing.

## Who uses this

- QA: primary
- Eng: optional second pass after self-review
- Pairs with `review-check-quality` (code anti-patterns) and `prepare-ci-ready-pr` (pipenv, pre-commit, PR etiquette)
