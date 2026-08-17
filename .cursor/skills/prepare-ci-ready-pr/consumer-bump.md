# Consumer Checkov image bumps

After Cloud Build publishes a new image tagged with `COMMIT_SHA`, open PRs in dependent repos so they pin that SHA.

## Config

Read `.cursor/checkov-consumers.yml`. Example shape:

```yaml
# Repos that consume this fork's Checkov image. Demo: keep the list to 1–2 entries.
image: us-central1-docker.pkg.dev/PROJECT/checkov/checkov
consumers:
  - repo: org/app-infra   # gh-style owner/name
    files:
      - path: cloudbuild.yaml
        # Optional regex; default replaces image:tag or image@sha for the configured image
      - path: .github/workflows/iac-scan.yml
  - repo: org/service-foo
    files:
      - path: deploy/checkov-job.yaml
```

If the file is missing, create it from this example with **placeholder** repos and ask the user to fill real `owner/name` paths before opening PRs.

## Procedure per consumer

1. `gh repo view <repo>` — confirm access.
2. Find current image reference in listed files.
3. Branch: `chore/bump-checkov-<shortsha>`
4. Replace tag/`latest`/old SHA with the new `COMMIT_SHA` (prefer tag form `image:COMMIT_SHA`).
5. Open PR:

```text
Title: chore: bump Checkov image to <COMMIT_SHA>

Body:
- Source Checkov commit / PR: …
- New image: <registry>/checkov:<COMMIT_SHA>
- Notable new checks (if any): CKV_…
```

6. Do not merge unless asked.

## Failure modes

- No write access → paste a manual patch and PR URL recipe
- File path wrong → search the consumer for the image string, then update the YAML
- Only `latest` in use → still bump to explicit SHA for auditability
