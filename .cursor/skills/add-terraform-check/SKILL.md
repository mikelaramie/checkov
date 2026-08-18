---
name: add-terraform-check
description: Implements a new Checkov Terraform check from a GitHub issue or GRC requirement, following CONTRIBUTING.md. Use when the user asks to add a check, implement an issue, turn a control into CKV_GCP or CKV2_GCP, or scaffold a policy from a GRC new check request.
---

# Add a Terraform check

Turn a GitHub issue or a stated requirement into a Checkov check plus tests. Follow [contributing.md](../contributing.md) / root `CONTRIBUTING.md`. Do not invent a Cloud Build (or other) runner here.

If the engineer has no working env yet (pipenv/pytest smoke test never run), point them to **`onboard-engineer`** first.

## SDLC

- Phase: design (steps 2–4), develop (steps 5–6), test (step 7)
- Must not: open a PR, push, invent a Cloud Build or other runner; skip the issue or mapping wait unless the engineer proceeds on recorded assumptions
- Next: `review-check-quality` (`Review my check before PR`); then `qa-fixture-review` / `prepare-ci-ready-pr`
- Source of truth: CONTRIBUTING.md — Open an issue; Tests for new checks

## Workflow

Copy and track:

```
- [ ] 1. Load the requirement (issue first)
- [ ] 2. Map the outcome to IaC features
- [ ] 3. Confirm pass/fail examples
- [ ] 4. Choose Python vs graph
- [ ] 5. Allocate the next ID
- [ ] 6. Implement from a nearby existing check
- [ ] 7. Add tests and run them per CONTRIBUTING
- [ ] 8. Stop for review (PR text ready, fast-lane)
```

### 1. Load the requirement

CONTRIBUTING expects contributors to **open an issue** with a detailed description and examples before coding.

If the user gives an issue number or URL:

```bash
gh issue view <n> --json title,body,labels
```

If there is **no issue**, draft one (or use `scope-contribution`) before implementing, unless the user explicitly wants a local-only spike. For a new check, ensure the issue has (or will get) the **`fast-lane`** label:

```bash
gh issue edit <n> --add-label "fast-lane"
```

Map GRC form headings to fields: Requirement title, Why it matters, Framework or control IDs, Cloud provider, Infrastructure as Code, Resource type, Category, Suggested severity, Passing/Failing example, Source links.

If **provider**, **resource type**, or **desired outcome** is missing, note it here and include it in the step 2 questions (do not invent a cloud).

This skill covers **Terraform**. If IaC is not Terraform, say so and stop.

### 2. Map the outcome to IaC features

GRC text often states a **business outcome** without naming Terraform arguments. Do not jump to HCL.

Before drafting examples, list:

1. **Outcome in Checkov language** (“Ensure …”).
2. **Candidate cloud/IaC features** that could implement it (more than one if the sentence is vague).
3. **The mapping you will use**, marked as an assumption if the issue did not name that feature.
4. **Questions** that would change the check (cloud scope, thresholds, storage class names, exceptions).

Show this list to the engineer. Do not silently pick `lifecycle_rule` vs `retention_policy`, Autoclass vs `SetStorageClass`, IAM binding vs member, or a single cloud when the request says “all.”

If the requirement came from a GitHub issue, **also post the same list on the issue** so GRC can answer there (not only in Cursor):

```bash
gh issue comment <n> --body "$(cat <<'EOF'
## Check mapping (needs GRC input)

**Proposed Checkov outcome:** …

**Clouds / resources in play:** … (or “unspecified — please confirm GCP / AWS / Azure / all”)

**Ways this could be implemented:**
- …
- …

**Questions**
1. …
2. …

Engineering will not encode a check until these are answered here or in the PR assumptions. Reply on this issue with your choices.
EOF
)"
```

Wait if the feature or cloud choice is ambiguous. If the engineer explicitly says to proceed on assumptions, keep those assumptions verbatim for the PR (step 8) and add a follow-up issue comment that lists what was assumed.

Example: “buckets must retain data 90 days and move to archive after 180” could be object lifecycle (`lifecycle_rule` Delete / `SetStorageClass` → `ARCHIVE`), Bucket Lock (`retention_policy`), Autoclass, or a combination — and on AWS/Azure the equivalent lifecycle/Object Lock/management policy. Name those options, then say which one you are encoding and why.

### 3. Confirm pass/fail examples

Need at least one passing and one failing Terraform resource (CONTRIBUTING: detailed examples on the issue).

- If the issue includes them, use those.
- If not, draft `main.tf` snippets from provider docs that match the **chosen** features from step 2, and **show the engineer** before writing production check files.

Name resources so tests can assert IDs (`google_storage_bucket.pass`, `google_storage_bucket.fail`).

### 4. Choose Python vs graph

Read [python-vs-graph.md](python-vs-graph.md). Default:

- One resource, one (or a few) attributes → Python in `checkov/terraform/checks/resource/<provider>/`
- Needs another resource to exist/connect, or AND/OR across types → YAML in `checkov/terraform/checks/graph_checks/<provider>/`

### 5. Allocate the next ID

Read [id-allocation.md](id-allocation.md). Search the repo for the prefix (`CKV_GCP_`, `CKV2_GCP_`, `CKV_AWS_`, …). Use **max + 1**. Do not reuse gaps. If contributing upstream, mention checking open PRs for the same next number.

### 6. Implement

Copy the closest existing check for that provider. Keep the change a **single coherent feature block** (CONTRIBUTING: rationalize commits).

**Python:** `name`, `id`, `supported_resources`, `categories`, then `check = ClassName()` at the bottom. Terraform attributes are list-wrapped (`encryption/[0]/default_kms_key_name`). Closest simple example: `checkov/terraform/checks/resource/gcp/CloudBuildWorkersArePrivate.py`. Any regex must use `re.compile` (CONTRIBUTING / flake8).

**YAML:** `metadata.id` / `name` / `category`, then `definition`. Connection example: `checkov/terraform/checks/graph_checks/gcp/GCPNetworkDoesNotUseDefaultFirewall.yaml`. Attribute-only example: `checkov/terraform/checks/graph_checks/gcp/GCPVertexAIPrivateEndpoint.yaml`.

Check `name` should be the positive outcome ("Ensure …").

### 7. Tests

Read [test-layout.md](test-layout.md). Match CONTRIBUTING “Tests for new checks”:

- Parse fixtures through `Runner` (not hand-built conf; see bad example `test_ALBListenerHTTPS.py`)
- Assert **resource ID sets** for pass and fail (counts alone are not enough)
- Canonical good example: `test_IAMAdminPolicyDocument.py`

Run tests with the **preferred** CONTRIBUTING commands when possible:

```bash
pipenv run pytest -k test_<Name>
# or with coverage:
pipenv run python -m coverage run -m pytest -k test_<Name>
```

Fallback if pipenv is unavailable: `.venv` + `pytest -k test_<Name> -o addopts=` (note the fallback). Fix failures before anything else.

Optional confidence check from CONTRIBUTING: build/install the local package and run `checkov` against the example fixtures.

### 8. Stop for review

Do not commit unless the user asked. Prefer running **`review-check-quality`** next (or apply that checklist). Then prepare PR text that matches `.github/PULL_REQUEST_TEMPLATE.md` and CONTRIBUTING PR rules:

- Title: `feat(terraform): add CKV_<PROVIDER>_<N> to <outcome>`
- `Fixes #<issue>` when an issue exists
- Label PR **`fast-lane`** for new checks
- Do not assign reviewers
- Policy description and how to fix in IaC; consider a short `docs/` note if useful
- **Assumptions / GRC clarifications:** cloud, resource, IaC features encoded, thresholds, exceptions, and any questions still open. Link the issue comment from step 2.

If you proceeded on assumptions, post a short issue comment with the same assumption list so GRC can still object after the PR is up.

For pre-commit, CI title/gates, and optional consumer image bumps, use **`prepare-ci-ready-pr`**. QA fixture coverage: **`qa-fixture-review`**.

## Additional resources

- [../contributing.md](../contributing.md) — CONTRIBUTING.md summary
- [python-vs-graph.md](python-vs-graph.md)
- [id-allocation.md](id-allocation.md)
- [test-layout.md](test-layout.md)
