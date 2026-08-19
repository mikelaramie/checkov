---
name: scope-contribution
description: Turns a PM or stakeholder brief into a scoped GitHub issue per CONTRIBUTING.md (examples, fast-lane for new checks) with acceptance criteria and the right Checkov contribution path. Use when a product manager, PM, or stakeholder describes a feature or requirement, asks to scope a change, write an issue from a brief, or route work to engineering, GRC, QA, or DevOps.
---

# Scope a contribution

Turn a short brief into a **scoped GitHub issue** (and next-skill pointer). Follow [contributing.md](../contributing.md) / root `CONTRIBUTING.md`: **open an issue first** with a detailed description and examples. Do not implement code in this skill.

## SDLC

- Phase: plan
- Must not: write check or test files; open an implementation PR
- Next: `add-terraform-check` (`Implement the check described in issue #N`); or `qa-fixture-review` when the issue is fixtures; or `maintain-ci-runners` (`Add a GitHub Actions gate for …` / `Bump consumers to Checkov SHA <sha>`) when the issue is CI/image
- Source of truth: CONTRIBUTING.md — Open an issue

## Workflow

```
- [ ] 1. Capture the brief
- [ ] 2. Classify the work
- [ ] 3. Draft acceptance criteria and examples
- [ ] 4. Open or update the issue (fast-lane when applicable)
- [ ] 5. Point to the next skill / owner
```

### 1. Capture the brief

From the user (or linked doc), extract:

- Problem / outcome
- Who cares (customer, audit, DX)
- Deadline or priority if stated
- Anything explicitly out of scope
- Passing / failing examples if known (CONTRIBUTING asks for examples)

If the outcome is unclear, ask **one** clarifying question before filing.

### 2. Classify

| Kind | Issue path | Next owner / skill |
|------|------------|-------------------|
| New compliance / security policy | **GRC new check request** form | Eng → `add-terraform-check` |
| Bug or wrong existing check | **Checks Issue** | Eng |
| Product / DX feature (not a check) | **Feature request** or scoped issue below | Eng |
| Test coverage / fixture gaps | Issue + QA notes | QA → `qa-fixture-review` |
| CI, image, consumer bump | **DevOps CI** form | DevOps → `maintain-ci-runners` |

Prefer the GRC form when the ask is a control/requirement without Terraform yet. Prefer **DevOps CI** when the ask is Cloud Build, GitHub Actions, Jenkins, or an image pin.

### 3. Acceptance criteria

Write 3–7 testable bullets. For checks, include:

- Cloud / IaC (or "TBD — eng will ask on issue")
- Pass and fail behavior in plain language
- At least a sketch of pass/fail examples (IaC or narrative) — CONTRIBUTING expects examples on the issue
- Exceptions if mentioned
- "Engineer records IaC assumptions on the PR"
- "PR and issue labeled `fast-lane`" for new checks

For non-checks: user-visible behavior, docs (`docs/` encouraged by CONTRIBUTING), and test expectations.

### 4. Open the issue

If GRC-shaped, guide the user to the form or create via `gh issue create` with body sections matching `.github/ISSUE_TEMPLATE/grc_new_check.yml` fields.

Otherwise:

```bash
gh issue create --title "<concise outcome>" --label "fast-lane" --body "$(cat <<'EOF'
## Summary
…

## Acceptance criteria
- [ ] …

## Examples
Passing: …
Failing: …

## Out of scope
- …

## Suggested skill / owner
- …

## References
- CONTRIBUTING.md
- …
EOF
)"
```

Use `--label "fast-lane"` for **new check** requests (CONTRIBUTING fast-lane). Omit it for unrelated DX/docs/CI work unless the team wants the same triage.

Include enough detail that maintainers can prioritize (CONTRIBUTING: popularity/effort/impact). Do not implement the change here.

### 5. Hand-off one-liner

Tell the user exactly what to say next, e.g.:

- `Implement the check described in issue #N` → `add-terraform-check`
- `Review fixtures for issue #N / PR #M` → `qa-fixture-review`
- `Make PR #M CI-ready` → `prepare-ci-ready-pr`
- `Add a GitHub Actions gate for …` / `Change Cloud Build to …` / `Bump consumers to Checkov SHA <sha>` → `maintain-ci-runners`

Remind eng that CONTRIBUTING expects local pipenv tests, pre-commit, and a `fast-lane` PR label for new checks.

## Who uses this

- PMs and stakeholders: primary
- Eng leads: triage a Slack/email brief into GitHub
