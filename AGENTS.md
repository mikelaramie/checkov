# Agent notes

This is Checkov: IaC policy-as-code. Shipped policies are **checks** (`CKV_*` / `CKV2_*`), not "controls."

## New engineers — first hour

1. Run **`onboard-engineer`** (prompt: `Set me up to contribute` / `Onboard me`).
2. Confirm smoke test: `test_IAMAdminPolicyDocument` passes.
3. Follow [`.cursor/skills/onboard-engineer/first-contribution.md`](.cursor/skills/onboard-engineer/first-contribution.md).
4. Implement with `add-terraform-check` → `review-check-quality` → `prepare-ci-ready-pr`.

Setup details and failures: [`.cursor/skills/onboard-engineer/troubleshooting.md`](.cursor/skills/onboard-engineer/troubleshooting.md).

- **Contribution guidelines (source of truth):** [`CONTRIBUTING.md`](CONTRIBUTING.md) — agent summary: [`.cursor/skills/contributing.md`](.cursor/skills/contributing.md)
- Prefer `pipenv install --dev`, `pipenv run … pytest`, and `pre-commit` (uv/.venv only as disclosed fallback)
- Python vs YAML checks: `docs/6.Contribution/`
- Cursor always-on context: `.cursor/rules/checkov-basics.mdc`

## Skills by persona

| Who | Goal | Skill |
|-----|------|--------|
| Eng (new) | Env, smoke test, first-hour path | `onboard-engineer` |
| Eng | Implement a Terraform check from an issue/GRC ask | `add-terraform-check` |
| Eng / QA | Pre-review: anti-patterns, weak tests | `review-check-quality` |
| Eng / DevOps | CI-ready PR, CONTRIBUTING etiquette, consumer image SHA bumps | `prepare-ci-ready-pr` |
| PM / lead | Brief → scoped GitHub issue + hand-off | `scope-contribution` |
| QA | Fixture / test-plan coverage for a check | `qa-fixture-review` |
| GRC | File the requirement | **GRC new check request** issue form |

Typical path: **onboard** → GRC or PM files issue (`fast-lane` for new checks) → eng `add-terraform-check` → `review-check-quality` / QA `qa-fixture-review` → `prepare-ci-ready-pr` → (optional) consumer bumps after Cloud Build.

All contribution skills must follow `CONTRIBUTING.md` (issue first, runner tests, resource ID assertions, pipenv/pre-commit preferred, no assigned reviewers, `fast-lane` for new checks).

## Adding a check (including from a GRC issue)

Use **add-terraform-check**. Typical prompt: `Implement the check described in issue #N`.

The skill posts mapping questions on the GitHub issue for GRC and records IaC features under **Assumptions / GRC clarifications** on the PR.

GRC: `.github/ISSUE_TEMPLATE/grc_new_check.yml`. Existing-check bugs: **Checks Issue**.

## Extending this system

Skills live in `.cursor/skills/<name>/SKILL.md` (optional reference `*.md` beside them). Rules live in `.cursor/rules/*.mdc`. Shared CONTRIBUTING summary: `.cursor/skills/contributing.md`.

To add a new workflow the team owns:

1. Copy a nearby skill directory; keep `SKILL.md` short; put detail in one-level reference files.
2. Write a third-person `description` with **what** and **when** (trigger phrases).
3. Link [contributing.md](.cursor/skills/contributing.md) when the skill touches issues, tests, or PRs.
4. Link it from this file's persona table and from any skill that should hand off to it.
5. If non-engineers start the work, add or point to a GitHub issue form under `.github/ISSUE_TEMPLATE/`.
6. Open a PR titled like `chore(general): add Cursor skill for …` (follow CONTRIBUTING PR etiquette).

Do not encode secrets or customer-private repos in skills. Consumer image targets go in `.cursor/checkov-consumers.yml`.
