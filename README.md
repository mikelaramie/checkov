# Custom Checkov engine image

Copy **all three files** to the root of [mikelaramie/checkov](https://github.com/mikelaramie/checkov):

| This file | In the fork |
|---|---|
| `Dockerfile` | `Dockerfile` (replace the upstream PyPI install) |
| `cloudbuild.yaml` | `cloudbuild.yaml` (Docker build/push, not the Terraform pipeline) |
| `.dockerignore` | `.dockerignore` (**required** — upstream excludes `checkov/` and `bin/`) |

Without the engine `.dockerignore`, `COPY . .` never includes `checkov/version.py` and `pip install .` fails.

The Cloud Build GitHub App must include the `checkov` repository. After a successful build, pin this consumer pipeline:

```yaml
_CHECKOV_IMAGE: "us-central1-docker.pkg.dev/mtothel-iac/checkov/checkov:<COMMIT_SHA>"
```
