---
name: prepare-ci-ready-pr
description: Prepares a Checkov change to pass CONTRIBUTING.md and repo CI gates—local pipenv/pre-commit tests, PR title and etiquette, fast-lane, and optional consumer image SHA bumps. Use when the user asks to make a PR CI-ready, follow contribution guidelines, fit the path to production, bump consumer Checkov image SHAs, or notify dependent repos after a Cloud Build.
---

# Prepare a CI-ready PR

Get a local change ready per [contributing.md](../contributing.md) / root `CONTRIBUTING.md` and this repo's CI. Stay inside [context-boundaries.md](context-boundaries.md).

## SDLC

- Phase: test (local pipenv/pre-commit), deploy (PR etiquette, `fast-lane`, optional consumer SHA bumps after Cloud Build)
- Must not: push or `gh pr create` unless the user asked; invent a new IaC runner; claim full matrix CI ran if it did not
- Next: human merge; after Cloud Build, optional consumer bumps (step 5)
- Source of truth: CONTRIBUTING.md — Creating a pull-request + fast-lane

## Workflow

```
- [ ] 1. Confirm scope, issue link, boundaries
- [ ] 2. Sync fork / base branch awareness
- [ ] 3. Run local checks (pipenv, pre-commit)
- [ ] 4. Draft PR title and body (CONTRIBUTING etiquette)
- [ ] 5. (Optional) Consumer image SHA bumps
- [ ] 6. Stop for human approval before push/PR
```

### 1. Confirm scope, issue, boundaries

Read [context-boundaries.md](context-boundaries.md). If the user asks for something outside the allowlist (new IaC runner, unrelated org repos, secrets), refuse or stop and ask.

Summarize: files touched, check IDs if any, linked issue.

CONTRIBUTING: contributions should start from an **issue** with examples. If there is no issue and this is not a trivial typo fix, say so and offer `scope-contribution` / open an issue first.

### 2. Sync

Remind the engineer to **keep the fork in sync** with `main` before opening a PR (CONTRIBUTING). If the branch is clearly behind, say so; do not force-push or rewrite history unless the user asks.

### 3. Local checks

Read [ci-gates.md](ci-gates.md). Minimum before claiming "CI-ready":

**Preferred (CONTRIBUTING)**

```bash
pipenv install --dev
pipenv run pytest -k <relevant>
# broader when feasible:
# pipenv run python -m coverage run -m pytest tests
pre-commit install   # once per clone
pre-commit run -a    # or at least on touched files if full run is too heavy—note what you ran
```

**Any check change**

1. Run `review-check-quality` (or that checklist).
2. Tests via pipenv as above (fallback: `.venv` / `uv` — disclose it).
3. Confirm PR title will match `.github/pr-title-checker-config.json`.

**Docs / rules / skills only**

- Title scope often `chore(general):` or `docs(general):`
- Still run `pre-commit` when practical
- No pytest required unless tests changed
- New or changed skills: `## SDLC` block present; linked from `AGENTS.md` persona table **and** SDLC table; four questions in `AGENTS.md` Extending this system are answered. See `.cursor/rules/skill-sdlc.mdc`.

Do not claim full matrix CI (all Python versions) ran locally unless it did.

Optional (CONTRIBUTING): local wheel build + `checkov --version` + scan example fixtures.

### 4. PR title and body

Title must match:

```text
^(fix|feat|break|docs|chore|platform)\((ansible|argo|arm|azure|bicep|bitbucket|circleci|cloudformation|dockerfile|github|gha|gitlab|helm|kubernetes|kustomize|openapi|sast|sca|secrets|serverless|terraform|general|graph|terraform_plan|terraform_json)\): 
```

Examples:

- `feat(terraform): add CKV_GCP_128 to ensure GCS lifecycle retains and archives`
- `chore(general): add Cursor skills for CI-ready PRs`

Body: follow `.github/PULL_REQUEST_TEMPLATE.md` **and** CONTRIBUTING:

- Reference related issues (`Fixes #N`)
- Explain non-obvious choices in the description or as a PR comment
- **Do not assign reviewers**
- New checks: add label **`fast-lane`**
- WIP: prefix `[WIP]` or use `/hold` until ready
- Encourage a short `docs/` addition when the change is user-facing
- Rationalize commits: one coherent feature for a new check when the user asks to commit

Do **not** push or `gh pr create` unless the user asked.

### 5. Optional: bump consumer Checkov images

After this repo's image is built (`cloudbuild.yaml` tags `${COMMIT_SHA}` and `latest`), DevOps may want PRs in dependent repos.

If the user asks to notify/bump consumers:

1. Read [consumer-bump.md](consumer-bump.md) and `.cursor/checkov-consumers.yml` (create from the example if missing).
2. For each listed repo, open a branch/PR that updates the Checkov image digest or tag to the new `COMMIT_SHA`.
3. PR body should link the Checkov commit/PR and list new check IDs when known.

Need `gh` auth and write access to those repos. Demo default: 1–2 repos in the YAML list.

### 6. Stop

Print:

- Suggested title (and WIP note if incomplete)
- Suggested body / labels (`fast-lane` when applicable)
- Local commands already run / still needed (`pipenv`, `pre-commit`)
- Consumer bump status (skipped / planned / PRs created)
- Reminder: ping maintainers on Slack only if the PR lacks attention (CONTRIBUTING)

## Who uses this

- Engineers: last mile before PR
- DevOps: step 5 after Cloud Build succeeds
