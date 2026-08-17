# CI gates (CONTRIBUTING + this repo)

Align with root [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) and [../contributing.md](../contributing.md). Exact GitHub runners may differ on forks.

## Title

- Workflow: `.github/workflows/pr-title.yml`
- Config: `.github/pr-title-checker-config.json`
- Must use allowed type + scope (see PR template comment block)

## Local quality (CONTRIBUTING)

Preferred:

```bash
pip install pipenv
pipenv install --dev
pipenv run python -m coverage run -m pytest tests
# targeted while iterating:
pipenv run pytest -k test_<ClassOrPolicyName>

pre-commit install
pre-commit run -a
```

CONTRIBUTING also documents optional conda (Python 3.10.x), local wheel build, and `checkov --version` against fixtures.

**Fallback** when pipenv is unavailable: `.venv` via `uv venv` / `uv pip install -e . pytest`, then:

```bash
pytest -k test_<ClassOrPolicyName> -o addopts=
```

(`pyproject.toml` may set xdist `addopts`; override if xdist is missing.) Always disclose when using the fallback.

## CI workflows (typical)

From `.github/workflows/pr-test.yml`:

- Pre-commit / lint
- DangerJS
- mypy
- Unit tests on multiple Python versions
- CFN lint when CloudFormation fixtures change

## Image build (deploy path)

Root `cloudbuild.yaml` builds and pushes:

- `${_AR_HOSTNAME}/${PROJECT_ID}/${_AR_REPO}/${_IMAGE}:${COMMIT_SHA}`
- `…:latest`

Consumer bumps should prefer the immutable `COMMIT_SHA` tag over `latest`.

## Do not claim

- Full PR matrix green without running it or seeing GitHub Checks
- Upstream Bridgecrew self-hosted runners behavior on a personal fork
- “CONTRIBUTING-compliant” if you skipped pipenv/pre-commit without noting the fallback
