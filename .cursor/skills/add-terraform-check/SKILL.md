---
name: add-terraform-check
description: Implements a new Checkov Terraform check from a GitHub issue or GRC requirement. Use when the user asks to add a check, implement an issue, turn a control into CKV_GCP or CKV2_GCP, or scaffold a policy from a GRC new check request.
---

# Add a Terraform check

Turn a GitHub issue or a stated requirement into a Checkov check plus tests. Do not invent a Cloud Build (or other) runner here.

## Workflow

Copy and track:

```
- [ ] 1. Load the requirement
- [ ] 2. Map the outcome to IaC features
- [ ] 3. Confirm pass/fail examples
- [ ] 4. Choose Python vs graph
- [ ] 5. Allocate the next ID
- [ ] 6. Implement from a nearby existing check
- [ ] 7. Add tests and run pytest
- [ ] 8. Stop for review (PR text ready)
```

### 1. Load the requirement

If the user gives an issue number or URL:

```bash
gh issue view <n> --json title,body,labels
```

Map GRC form headings to fields: Requirement title, Why it matters, Framework or control IDs, Cloud provider, Infrastructure as Code, Resource type, Category, Suggested severity, Passing/Failing example, Source links.

If there is no issue, use the user's description. If **provider**, **resource type**, or **desired outcome** is missing, note it here and include it in the step 2 questions (do not invent a cloud).

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

Need at least one passing and one failing Terraform resource.

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

Copy the closest existing check for that provider.

**Python:** `name`, `id`, `supported_resources`, `categories`, then `check = ClassName()` at the bottom. Terraform attributes are list-wrapped (`encryption/[0]/default_kms_key_name`). Closest simple example: `checkov/terraform/checks/resource/gcp/CloudBuildWorkersArePrivate.py`.

**YAML:** `metadata.id` / `name` / `category`, then `definition`. Connection example: `checkov/terraform/checks/graph_checks/gcp/GCPNetworkDoesNotUseDefaultFirewall.yaml`. Attribute-only example: `checkov/terraform/checks/graph_checks/gcp/GCPVertexAIPrivateEndpoint.yaml`.

Check `name` should be the positive outcome ("Ensure …").

### 7. Tests

Read [test-layout.md](test-layout.md). Parse fixtures through `Runner`, assert resource ID sets. Then:

```bash
pytest -k test_<Name>
```

Fix failures before anything else.

### 8. Stop for review

Do not commit unless the user asked. Prepare PR text that matches `.github/PULL_REQUEST_TEMPLATE.md`, including:

- Title: `feat(terraform): add CKV_<PROVIDER>_<N> to <outcome>`
- `Fixes #<issue>` when an issue exists
- Policy description and how to fix in IaC
- **Assumptions / GRC clarifications:** cloud, resource, IaC features encoded, thresholds, exceptions, and any questions still open. Link the issue comment from step 2.

If you proceeded on assumptions, post a short issue comment with the same assumption list so GRC can still object after the PR is up.

## Additional resources

- [python-vs-graph.md](python-vs-graph.md)
- [id-allocation.md](id-allocation.md)
- [test-layout.md](test-layout.md)
