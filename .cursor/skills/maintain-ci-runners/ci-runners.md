# CI/CD runners in this repo

Two different “runners”:

| Kind | Meaning | Owner |
|------|---------|--------|
| Checkov **IaC** runner | Parser/scanner (`checkov/terraform/`, Kubernetes, …) | Eng — not this skill |
| **CI/CD** runner | Cloud Build, GitHub Actions, Jenkins, CircleCI | DevOps — this skill |

CONTRIBUTING.md notes that many users run Checkov locally or via Jenkins/CircleCI. Do not treat that as permission to add a Jenkinsfile unless the issue asks for one.

## This repository

| Path | Role |
|------|------|
| `cloudbuild.yaml` | Build/push image tags `${COMMIT_SHA}` and `latest` |
| `.github/workflows/pr-test.yml` | PR lint, DangerJS, mypy, unit-test matrix, CFN lint |
| `.github/workflows/pr-title.yml` | PR title gate (config: `.github/pr-title-checker-config.json`) |
| `.github/workflows/*.yml` | Nightly, coverage, CodeQL, security, docs, pipenv update |
| `.pre-commit-config.yaml` | Local + CI lint hooks |
| `docs/4.Integrations/Jenkins.md` | Public Jenkins example using the Checkov image |

Ignore workflow YAML under `tests/` and `integration_tests/` — those are fixtures, not CI.

## When adding a gate

1. **Local contributor command** → `CONTRIBUTING.md` first, then skill summaries (`contributing.md`, `prepare-ci-ready-pr` `ci-gates.md`, `onboard-engineer` if install is required).
2. **GitHub Actions / Cloud Build only** → workflow or `cloudbuild.yaml`; say in the PR that local CONTRIBUTING commands are unchanged.
3. **How consumers run Checkov** → `docs/4.Integrations/` (and bump consumer pins with [consumer-bump.md](consumer-bump.md) after the image exists).

## Do not

- Add a new Checkov IaC framework to ship a pipeline
- Store secrets, keys, or `.env` values in workflows or skills
- Claim upstream Bridgecrew self-hosted runner behavior on a personal fork
- Edit consumer repos not listed in `.cursor/checkov-consumers.yml` unless the user names them
