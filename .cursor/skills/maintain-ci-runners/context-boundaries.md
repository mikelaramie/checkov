# Context boundaries (DevOps)

Approved sources for `maintain-ci-runners`. Stay inside this fence unless the user explicitly expands it.

## Allow

- This repository: `cloudbuild.yaml`, `.github/workflows/` (not test fixtures), `.pre-commit-config.yaml`, `docs/4.Integrations/`
- Root `CONTRIBUTING.md` and `.cursor/skills/contributing.md`
- GitHub for **this** repo: issues, PRs, Actions checks (`gh`)
- Files under `.cursor/` (rules, skills, `checkov-consumers.yml`)
- Consumer repos **listed** in `.cursor/checkov-consumers.yml`, or named by the user, for image-pin PRs only
- Linked DevOps / CI issues on this repo

## Deny (unless user explicitly asks)

- Implementing `CKV_*` / `CKV2_*` checks or a new Checkov IaC runner
- Cloning or searching unrelated private customer monorepos
- Opening PRs to consumer repos not listed in `.cursor/checkov-consumers.yml`
- Reading secrets, credentials, `.env`, or cloud keys
- Force-push, skipping hooks, or changing git config
- Inventing contributor process that contradicts `CONTRIBUTING.md`

## When blocked

Say what was requested, why it is out of bounds, and the in-repo alternative (`add-terraform-check` for policies, extend `checkov-consumers.yml`, file a DevOps CI issue).
