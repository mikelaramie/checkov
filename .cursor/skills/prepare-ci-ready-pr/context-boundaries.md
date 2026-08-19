# Context boundaries

Approved sources the agent may use for Checkov contribution skills. Stay inside this fence unless the user explicitly expands it.

## Allow

- This repository (working tree, `git`, local tests)
- Root `CONTRIBUTING.md` and `.cursor/skills/contributing.md`
- GitHub for **this** repo: issues, PRs, Actions checks (`gh`)
- Public provider docs needed to draft pass/fail Terraform (GCP/AWS/Azure resource docs)
- Files under `.cursor/` (rules, skills, `checkov-consumers.yml`)
- Linked GRC / PM / QA issues on this repo

## Deny (unless user explicitly asks)

- Cloning or searching unrelated private customer monorepos
- Inventing or editing a CI/CD **runner** (Cloud Build, Jenkins, GitHub Actions) here or in `add-terraform-check` — that is `maintain-ci-runners`
- Reading secrets, credentials, `.env`, or cloud keys
- Force-push, skipping hooks, or changing git config
- Opening PRs to consumer repos not listed in `.cursor/checkov-consumers.yml` (or named by the user)
- Pulling policy text from random web pages when the issue already states the requirement

## When blocked

Say what was requested, why it is out of bounds, and what in-repo alternative exists (file an issue, `maintain-ci-runners` for CI/CD, extend consumers YAML, use a different skill).
