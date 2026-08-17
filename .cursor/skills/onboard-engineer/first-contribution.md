# First hour after setup

Ordered path for a new engineer once `onboard-engineer` smoke test passes.

## 30–60 minute sequence

1. **Skim** root [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) “Tests for new checks” (runner fixtures, resource ID assertions).
2. **Read** the golden test: `tests/terraform/checks/resource/aws/test_IAMAdminPolicyDocument.py` and its `example_IAMAdminPolicyDocument/` fixtures.
3. **Skim** a simple GCP Python check: `checkov/terraform/checks/resource/gcp/CloudBuildWorkersArePrivate.py`.
4. **Pick work:**
   - Existing `fast-lane` / GRC issue → `Implement the check described in issue #N`
   - No issue → file one (GRC form or starter brief below) → then the same prompt
5. **Implement** with `add-terraform-check`.
6. **Self-review** with `review-check-quality` (QA may use `qa-fixture-review`).
7. **PR** with `prepare-ci-ready-pr` (pipenv tests, pre-commit, title, `fast-lane`).

## Starter brief (hello contribution)

Use when there is no issue yet. File via **GRC new check request** or `scope-contribution`, label **`fast-lane`**, then implement. Prefer a **real team / GRC requirement** over inventing work.

**Before filing:** search the repo for an existing check (`CKV_GCP_`, resource type, or keyword). Example already shipped: `GoogleStorageBucketUniformAccess` (`uniform_bucket_level_access`) — **study it**, do not re-implement.

**Practice options (pick one):**

1. Mentor or GRC assigns a real `fast-lane` issue → implement that.
2. Open a **Checks Issue** for a small bug/docs fix on an existing check (good first PR without new IDs).
3. If inventing a demo requirement, state cloud + resource + outcome, search for duplicates, then file—e.g. a single-attribute GCP/AWS setting your team cares about that is **not** already a `CKV_*`.

**Study pair (do not copy IDs):**

- Check: `checkov/terraform/checks/resource/gcp/CloudBuildWorkersArePrivate.py`
- Test style: `tests/terraform/checks/resource/aws/test_IAMAdminPolicyDocument.py`

**Examples on the issue:** Engineer drafts pass/fail `main.tf` during `add-terraform-check` step 3 if GRC left them blank.

## Mental model

| Term | Meaning |
|------|---------|
| Check / policy | Shipped rule (`CKV_*` / `CKV2_*`), not “control” |
| Python check | One resource’s attributes |
| Graph check (`CKV2_*`) | Connections / multi-resource logic |
| Runner test | Parse real IaC; assert resource ID sets |

## Skills cheat sheet

| Prompt | Skill |
|--------|--------|
| Set up my environment | `onboard-engineer` |
| Scope this brief into an issue | `scope-contribution` |
| Implement issue #N | `add-terraform-check` |
| Review my check before PR | `review-check-quality` |
| Are the fixtures enough? | `qa-fixture-review` |
| Make this PR CI-ready | `prepare-ci-ready-pr` |
