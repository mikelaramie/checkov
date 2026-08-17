---
name: onboard-engineer
description: Sets up a new engineer to contribute to Checkov—clone sync, pipenv or uv fallback, pre-commit, smoke test, and first-hour skill path. Use when onboarding, setting up the dev environment, getting started, first contribution, day one, or when pipenv/pytest/pre-commit setup fails.
---

# Onboard an engineer

Get from empty machine (or fresh clone) to **ready for `add-terraform-check`**. Follow [../contributing.md](../contributing.md) / root `CONTRIBUTING.md`. Read [troubleshooting.md](troubleshooting.md) when a step fails.

## Workflow

```
- [ ] 1. Prerequisites
- [ ] 2. Repo and branch
- [ ] 3. Python env (pipenv preferred)
- [ ] 4. Pre-commit hooks
- [ ] 5. Smoke test
- [ ] 6. Optional CLI sanity
- [ ] 7. First-hour hand-off
```

### 1. Prerequisites

Confirm or help install:

| Tool | Why |
|------|-----|
| Git | Clone / branch |
| Python 3.9–3.13 (CONTRIBUTING examples often use 3.10.x) | Runtime |
| `pip` | Install pipenv |
| GitHub CLI `gh` (recommended) | Issues / PRs |
| pipenv **or** uv (fallback) | Dev deps |

On Windows: prefer running from the repo root in PowerShell or Git Bash; see [troubleshooting.md](troubleshooting.md).

### 2. Repo and branch

```bash
git status
git fetch origin
git checkout main
git pull origin main
```

If this is a fork, remind them to sync with upstream weekly (CONTRIBUTING). Create a feature branch only when starting real work—not required to finish onboarding.

### 3. Python env (preferred = CONTRIBUTING)

```bash
pip install pipenv
pipenv install --dev
```

**Fallback** if pipenv is missing or broken (disclose in the hand-off):

```bash
uv venv .venv --python 3.12
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
uv pip install -e . pytest
# If pytest fails on xdist addopts:
#   pytest -k … -o addopts=
```

Do not invent a third package manager. Prefer documenting which path succeeded.

### 4. Pre-commit

```bash
pre-commit install
# Optional full run (can be slow on first install):
# pre-commit run -a
```

If `pre-commit` is not on PATH, `pipenv run pre-commit install` or install via the active venv.

### 5. Smoke test

Prove the canonical CONTRIBUTING test style runs:

```bash
pipenv run pytest -k test_IAMAdminPolicyDocument -o addopts=
```

Fallback:

```bash
pytest tests/terraform/checks/resource/aws/test_IAMAdminPolicyDocument.py -o addopts=
```

**Pass** = onboarding env OK. **Fail** → [troubleshooting.md](troubleshooting.md); do not proceed to implement checks.

### 6. Optional CLI sanity (CONTRIBUTING)

```bash
pipenv run checkov --version
# or after editable install: checkov --version
```

Skip if time-boxed; smoke test is enough for “ready.”

### 7. First-hour hand-off

Show [first-contribution.md](first-contribution.md). End with:

```markdown
## Onboarding complete

- Env: pipenv | uv/.venv (fallback)
- Smoke test: test_IAMAdminPolicyDocument — PASS | FAIL
- Pre-commit: installed | skipped (reason)

**Next prompt:** Implement the check described in issue #N
(or file a starter issue from first-contribution.md, then use add-terraform-check)

**Path:** add-terraform-check → review-check-quality → prepare-ci-ready-pr
```

Do not implement a production check in this skill unless the user explicitly asks after setup.

## Who uses this

- New engineers (primary)
- Mentors: “run onboard-engineer for this clone”
