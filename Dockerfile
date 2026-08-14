# Copy these two files to the root of https://github.com/mikelaramie/checkov
# (Dockerfile and cloudbuild.yaml). The upstream Dockerfile installs Checkov
# from PyPI; this one installs the repo source so core-check changes ship in the image.

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
