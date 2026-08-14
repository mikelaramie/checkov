# Copy Dockerfile, cloudbuild.yaml, and .dockerignore to the root of
# https://github.com/mikelaramie/checkov. Upstream .dockerignore excludes
# checkov/ (PyPI install); this image installs from source.

FROM python:3.11-slim

ENV RUN_IN_DOCKER=True \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /src

RUN apt-get update \
    && apt-get install -y --no-install-recommends git gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir .

ENTRYPOINT ["checkov"]
