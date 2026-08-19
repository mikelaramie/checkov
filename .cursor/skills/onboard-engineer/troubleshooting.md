# Onboarding troubleshooting

Use when `onboard-engineer` steps fail. Prefer fixing the **preferred** CONTRIBUTING path before leaning on fallbacks.

## `pipenv` not found

- Install: `pip install pipenv` (same Python you will develop with).
- Windows: ensure that Python’s `Scripts` directory is on `PATH`, or use `python -m pip install pipenv` then `python -m pipenv …`.
- If still blocked, use **uv/.venv fallback** and say so in the hand-off.

## `ModuleNotFoundError: checkov` / `yaml` / similar

- Editable install missing: `pipenv install --dev` or `uv pip install -e .`
- Running pytest with the wrong interpreter (system Python vs venv). Activate or prefix with `pipenv run`.

## `pytest` unrecognized args: `-n` / `--dist`

`pyproject.toml` may set `addopts = "-n 2 --dist loadfile"` (pytest-xdist). If xdist is not installed:

```bash
pipenv run pytest -k test_IAMAdminPolicyDocument -o addopts=
# or
pytest -k test_IAMAdminPolicyDocument -o addopts=
```

Dev install via `pipenv install --dev` should pull xdist; override is fine for smoke tests.

## Smoke test fails on assertion / import inside Checkov

- Update `main`: `git pull`
- Confirm cwd is repo root
- Re-run with: `pipenv run pytest tests/terraform/checks/resource/aws/test_IAMAdminPolicyDocument.py -vv -o addopts=`
- If only this machine fails, capture the traceback; do not “fix” upstream checks during onboarding

## `pre-commit` not found / hooks not running

```bash
pipenv run pip install pre-commit
pipenv run pre-commit install
```

Or install `pre-commit` into the active venv. CI still runs lint even if local hooks are missing—local install is still expected by CONTRIBUTING.

## Windows-specific

- Prefer PowerShell or Git Bash at repo root (`C:\…\checkov`).
- Activation: `.venv\Scripts\Activate.ps1` (may need `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once).
- Path separators in docs are POSIX-style; Shell accepts either in most tools.
- If `gh` is missing: install GitHub CLI or use the GitHub web UI for issues until installed.

## Slow `pipenv install --dev` / `pre-commit run -a`

Normal on first run. For onboarding, smoke pytest + `pre-commit install` is enough; defer full `pre-commit run -a` until `prepare-ci-ready-pr`.

## Wrong skill after setup

| Symptom | Skill |
|---------|--------|
| Need a scoped GitHub issue | `scope-contribution` |
| Ready to implement CKV check | `add-terraform-check` |
| Env works but tests look wrong | `review-check-quality` / `qa-fixture-review` |
| Ready to open PR | `prepare-ci-ready-pr` |
| Cloud Build / Actions / Jenkins / image pin | `maintain-ci-runners` |
