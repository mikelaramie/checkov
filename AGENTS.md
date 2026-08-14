# Agent notes

This is Checkov: IaC policy-as-code. Shipped policies are **checks** (`CKV_*` / `CKV2_*`), not "controls."

## New engineers

- Setup and tests: `CONTRIBUTING.md`
- Python vs YAML checks: `docs/6.Contribution/`
- Cursor always-on context: `.cursor/rules/checkov-basics.mdc`

## Adding a check (including from a GRC issue)

Use the **add-terraform-check** skill. Typical prompt: `Implement the check described in issue #N`.

The skill posts mapping questions on the GitHub issue for GRC and records the chosen IaC features under **Assumptions / GRC clarifications** on the PR.

GRC files requests with **GRC new check request** (`.github/ISSUE_TEMPLATE/grc_new_check.yml`). Existing-check bugs still use **Checks Issue**.
