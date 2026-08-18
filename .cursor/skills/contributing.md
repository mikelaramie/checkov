# CONTRIBUTING.md (source of truth)

All contribution skills must follow the repo root [`CONTRIBUTING.md`](../../CONTRIBUTING.md) (upstream: [bridgecrewio/checkov CONTRIBUTING.md](https://github.com/bridgecrewio/checkov/blob/main/CONTRIBUTING.md)). Prefer that file over inventing process. Summarized here for agents; if this summary and the file disagree, **follow the file**.

## Before coding

1. **Open an issue first** with a detailed description and examples (CONTRIBUTING: Open an issue).
2. For a **new check**, label the issue `fast-lane` so maintainers see it quickly.
3. Work on a **local fork/clone**; test locally before opening a PR.
4. **Keep the fork in sync** with `main` (upstream updates often weekly).

## Environment and tests (preferred)

Official path from CONTRIBUTING:

```sh
# Optional: conda with Python 3.10.x
conda create -n python310 python=3.10.17
conda activate python310

pip install pipenv
pipenv install --dev
pipenv run python -m coverage run -m pytest tests
# or targeted:
pipenv run pytest -k test_<Name>
```

Pre-commit (required before claiming lint-ready):

```shell
pre-commit install
pre-commit run -a
```

**Fallback** (demo / pipenv unavailable): project `.venv` via `uv` or `pip install -e . pytest`, then `pytest -k … -o addopts=` if xdist is missing. Say when you used the fallback.

## Tests for new checks (non-negotiable)

From CONTRIBUTING “Tests for new checks”:

- Parse templates through the **runner** (files or string templates). Canonical: `tests/terraform/checks/resource/aws/test_IAMAdminPolicyDocument.py`.
- **Do not** hard-code conf objects. Bad example called out upstream: `test_ALBListenerHTTPS.py`.
- Assert **which resources** pass and fail — counts alone are not enough.
- Unit tests live under `tests/`. E2E is optional for simple checks but helps readiness.

## Implementation notes from CONTRIBUTING

- Use `re.compile` for all regex (flake8).
- Docs under `docs/` are encouraged (not mandatory) for important contributions.
- Rationalize commits: one coherent feature block for a new check; logical blocks for fixes.

## Pull requests

From CONTRIBUTING “Creating a pull-request” + fast-lane:

- Reference related issues (`Fixes #N`).
- Comment on the PR where something needs explanation.
- Do **not** assign explicit reviewers (maintainers triage).
- WIP: prefix title with `[WIP]` or use `/hold`.
- New checks: label the PR `fast-lane`.
- Trivial doc fixes: fix related mistakes in the same doc; avoid many tiny PRs for one file.
- Optional: build wheel / `checkov --version` and run fixtures via CLI (see CONTRIBUTING) for extra confidence.

## Skill mapping

| CONTRIBUTING topic | SDLC phase | Primary skill |
|--------------------|------------|---------------|
| Clone, pipenv/pre-commit, first smoke test | before plan | `onboard-engineer` |
| Open issue, examples, fast-lane on issue | plan | `scope-contribution` |
| Map IaC features, implement check + runner tests | design / develop / test | `add-terraform-check` |
| Test standard / anti-patterns | review | `review-check-quality`, `qa-fixture-review` |
| Local test, pre-commit, PR etiquette, fast-lane on PR | test / deploy | `prepare-ci-ready-pr` |

Phase contract (must-not, next prompt): root [`AGENTS.md`](../../AGENTS.md) SDLC table. Every skill `SKILL.md` must include `## SDLC`. Authoring skills/rules: `.cursor/rules/skill-sdlc.mdc`.
