---
name: maintain-ci-runners
description: Maintains Checkov CI/CD pipelines (Cloud Build, GitHub Actions, Jenkins examples) and post-merge consumer image SHA bumps. Use when DevOps asks to add or change a CI gate, edit cloudbuild.yaml or GitHub Actions, integrate Jenkins, bump consumer Checkov images after Cloud Build, or notify dependent repos.
---

# Maintain CI/CD runners

Own **CI/CD pipelines** and **post-merge image pins**. Follow [contributing.md](../contributing.md) / root `CONTRIBUTING.md`. Stay inside [context-boundaries.md](context-boundaries.md).

This is not a Checkov **IaC** runner (Terraform/Kubernetes parsers). Those stay with engineering. Do not implement `CKV_*` / `CKV2_*` checks here.

## SDLC

- Phase: develop (pipeline files in this repo), deploy (consumer SHA bumps after merge + image build)
- Must not: implement CKV/CKV2 checks; invent a Checkov IaC runner; skip CONTRIBUTING.md when adding a contributor-facing local gate; bump repos outside `.cursor/checkov-consumers.yml` unless the user names them; claim the full pytest matrix ran if it did not
- Next: after pipeline edits, `prepare-ci-ready-pr` (`Make this PR CI-ready`); after consumer PRs, human merge
- Source of truth: CONTRIBUTING.md — Open an issue; Creating a pull-request; local Jenkins/CircleCI mention under Work locally

**Stop between tracks.** Finish pipeline edits and hand off to `prepare-ci-ready-pr` before opening that PR. Do not bump consumers until the Checkov image for the merged SHA exists.

## Workflow

```
- [ ] 1. Classify the ask
- [ ] 2. Confirm issue and boundaries
- [ ] 3. Pipeline track (develop) — or skip
- [ ] 4. STOP: prepare-ci-ready-pr for pipeline PRs
- [ ] 5. Consumer-bump track (deploy) — or skip
- [ ] 6. Stop for human approval
```

### 1. Classify

| Ask | Track | Exact next prompt after this skill |
|-----|--------|--------------------------------------|
| Add/change Cloud Build, GitHub Actions, pre-commit CI, Jenkins example | Pipeline | `Make this PR CI-ready` → `prepare-ci-ready-pr` |
| Pin consumers to a new Checkov image SHA | Consumer bump | Human merge of consumer PRs |
| Both | Pipeline first, then bump after merge + image | Same as above, in order |

If the user is implementing a **check**, stop and point to `add-terraform-check`.

### 2. Issue and boundaries

Read [context-boundaries.md](context-boundaries.md). CONTRIBUTING: start from an **issue** with examples. If there is none and this is not a trivial typo, say so and offer `scope-contribution` or the **DevOps CI** issue form.

Summarize: files to touch, which runner (Cloud Build / Actions / Jenkins docs), linked issue.

### 3. Pipeline track (develop)

Read [ci-runners.md](ci-runners.md). Edit only the files that match the ask.

**Contributor-facing gate** (engineers must run a new local command before a PR): update root `CONTRIBUTING.md` first, then `.cursor/skills/contributing.md` and `prepare-ci-ready-pr` `ci-gates.md`. If it must be installed on day one, also `onboard-engineer`. Do not claim CONTRIBUTING already requires the tool if it does not.

**This-repo CI only** (workflow that GitHub/Cloud Build runs): prefer `.github/workflows/` or `cloudbuild.yaml`. Mention the change in the PR body.

**Jenkins / consumer how-to:** prefer `docs/4.Integrations/` (Jenkins is documented there; this repo has no Jenkinsfile).

Do not invent a new Checkov IaC framework under `checkov/`.

### 4. STOP (pipeline PRs)

Do not push or `gh pr create` unless the user asked. Hand off:

`Make this PR CI-ready` → **`prepare-ci-ready-pr`**

That skill owns title, pre-commit, and etiquette. This skill must not claim the PR is CI-ready.

### 5. Consumer-bump track (deploy)

Only after merge **and** Cloud Build has published `${COMMIT_SHA}` (see `cloudbuild.yaml`).

Read [consumer-bump.md](consumer-bump.md) and `.cursor/checkov-consumers.yml`. Open bump PRs only for listed repos (or repos the user named). Prefer the immutable `COMMIT_SHA` tag over `latest`.

Need `gh` auth and write access. Demo default: 1–2 entries in the YAML.

Do not merge consumer PRs unless asked.

### 6. Stop

Print:

- Track(s) run (pipeline / consumer bump)
- Files or consumer repos touched
- Linked issue
- Pipeline PRs: reminder to run `prepare-ci-ready-pr`
- Consumer PRs: URLs or a manual patch if access failed
- CONTRIBUTING.md / `ci-gates.md` updates still needed, if any

## Who uses this

- DevOps / platform: primary
- Eng: only when the ask is a pipeline or image pin, not a check

## Additional resources

- [../contributing.md](../contributing.md) — CONTRIBUTING.md summary
- [ci-runners.md](ci-runners.md)
- [consumer-bump.md](consumer-bump.md)
- [context-boundaries.md](context-boundaries.md)
