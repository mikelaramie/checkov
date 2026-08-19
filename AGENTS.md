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
| Eng | CI-ready PR, CONTRIBUTING etiquette | `prepare-ci-ready-pr` |
| DevOps | Cloud Build / GitHub Actions / Jenkins CI, consumer image SHA bumps | `maintain-ci-runners` |
| PM / lead | Brief → scoped GitHub issue + hand-off | `scope-contribution` |
| QA | Fixture / test-plan coverage for a check | `qa-fixture-review` |
| GRC | File the requirement | **GRC new check request** issue form |

Typical path: **onboard** → GRC or PM files issue (`fast-lane` for new checks) → eng `add-terraform-check` → `review-check-quality` / QA `qa-fixture-review` → `prepare-ci-ready-pr` → human merge → DevOps `maintain-ci-runners` after Cloud Build (optional consumer bumps). CI/pipeline asks: **DevOps CI** form or `scope-contribution` → `maintain-ci-runners` → `prepare-ci-ready-pr`.

All contribution skills must follow `CONTRIBUTING.md` (issue first, runner tests, resource ID assertions, pipenv/pre-commit preferred, no assigned reviewers, `fast-lane` for new checks).

## SDLC (plan → design → develop → review → test → deploy)

Skills are prompt-time guidance. Order holds only if each skill **refuses later-phase work** and names the next skill. `CONTRIBUTING.md` still wins when a skill summary disagrees.

| Phase | Owner | Must not | Next |
|-------|--------|----------|------|
| *(before plan)* | `onboard-engineer` | Implement a production check | `scope-contribution` or `add-terraform-check` |
| **Plan** | `scope-contribution`, GRC new check request form, DevOps CI form | Write check or test files | `Implement the check described in issue #N` → `add-terraform-check`; CI/image → `Add a GitHub Actions gate for …` / `Bump consumers to Checkov SHA <sha>` → `maintain-ci-runners` |
| **Design** | `add-terraform-check` steps 2–4 (IaC mapping, examples, Python vs graph) | Allocate IDs or implement until mapping is posted, unless the engineer proceeds on recorded assumptions | same skill, develop steps |
| **Develop** (checks) | `add-terraform-check` steps 5–6 | Open a PR, push, invent a Cloud Build/Jenkins/GitHub Actions runner | tests in step 7, then review |
| **Develop** (CI/CD) | `maintain-ci-runners` (pipeline files) | Write CKV checks; invent a Checkov IaC runner; skip CONTRIBUTING.md for a new contributor-facing gate | `Make this PR CI-ready` → `prepare-ci-ready-pr` |
| **Review** | `review-check-quality` (code), `qa-fixture-review` (fixtures) | Claim CI-ready; QA must not rewrite production check logic unless asked | `Make this PR CI-ready` → `prepare-ci-ready-pr` |
| **Test** | Develop step 7, review targeted pytest, `prepare-ci-ready-pr` local pipenv/pre-commit, then GitHub CI | Skip runner-parsed fixtures or resource ID assertions | deploy |
| **Deploy** (PR) | `prepare-ci-ready-pr` (PR title/etiquette, `fast-lane`) | Push or `gh pr create` unless asked; edit CI runners or bump consumers; claim full matrix CI ran if it did not | human merge; then DevOps if an image pin is needed |
| **Deploy** (post-merge) | `maintain-ci-runners` (consumer SHA bumps) | Write CKV checks; bump repos not in `.cursor/checkov-consumers.yml` unless the user names them | human merge of consumer PRs |

Always-on `.cursor/rules/checkov-basics.mdc` names this path. Glob rules on check files are **develop-phase** only. Authoring skills/rules: `.cursor/rules/skill-sdlc.mdc`.

## Adding a check (including from a GRC issue)

Use **add-terraform-check**. Typical prompt: `Implement the check described in issue #N`.

The skill posts mapping questions on the GitHub issue for GRC and records IaC features under **Assumptions / GRC clarifications** on the PR.

GRC: `.github/ISSUE_TEMPLATE/grc_new_check.yml`. Existing-check bugs: **Checks Issue**. CI/CD and image pins: **DevOps CI** (`.github/ISSUE_TEMPLATE/devops_ci.yml`) → `maintain-ci-runners`.

## Extending this system

Skills live in `.cursor/skills/<name>/SKILL.md` (optional reference `*.md` beside them). Rules live in `.cursor/rules/*.mdc`. Shared CONTRIBUTING summary: `.cursor/skills/contributing.md`.

To add a new workflow the team owns:

1. Copy a nearby skill directory; keep `SKILL.md` short; put detail in one-level reference files.
2. Write a third-person `description` with **what** and **when** (trigger phrases).
3. Link [contributing.md](.cursor/skills/contributing.md) when the skill touches issues, tests, or PRs.
4. Link it from this file's **persona table**, **SDLC table**, and from any skill that should hand off to it.
5. If non-engineers start the work, add or point to a GitHub issue form under `.github/ISSUE_TEMPLATE/` (GRC new check request, Contribution scope, DevOps CI).
6. Add a `## SDLC` block to `SKILL.md` (template below).
7. Answer the four questions. If a skill can finish a later phase without naming the later skill, add a hard stop or split it.
8. Open a PR titled like `chore(general): add Cursor skill for …` (follow CONTRIBUTING PR etiquette). Use `prepare-ci-ready-pr`.

### Required `## SDLC` block

```markdown
## SDLC
- Phase: plan | design | develop | review | test | deploy
- Must not: <later-phase work this skill is forbidden to do>
- Next: `<skill>` (`<exact user prompt>`)
- Source of truth: CONTRIBUTING.md — <section>
```

Use `Phase: before plan` only for environment setup (`onboard-engineer`). If one skill spans two phases (for example design+develop), list both and put a **stop** between them.

### Four questions (skill/rule PRs)

1. **Which one phase is this?** If several, split or add hard stops between steps.
2. **What must this skill refuse?** Plan must not write checks; develop must not open the PR; review must not claim CI-ready.
3. **What is the exact next prompt?** Example: `Implement the check described in issue #N`.
4. **Does CONTRIBUTING.md still win?** Skills summarize; they must not invent process.

Do not encode secrets or customer-private repos in skills. Consumer image targets go in `.cursor/checkov-consumers.yml`.
