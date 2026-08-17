"""GCP label field aliases for YAML `taggable` policies.

Most Google provider resources expose a top-level `labels` map. A few APIs use a
different argument (`resource_labels`, `user_labels`, or nested
`settings.user_labels`). Custom policies almost always write `attribute: labels`
(see docs/3.Custom Policies). Without an alias, those resources would be scanned
after being added to `gcp_taggable` and then miss their actual label field.

This module is the source of truth for:
- which Terraform paths count as GCP resource labels
- which resource types are appended to `gcp_taggable`

Not treated as GCP labels: Kubernetes node `node_config.labels`. AWS `tags` are
unchanged. Empty maps still satisfy operator `exists` (same as AWS `tags`); use
`is_not_empty` when at least one key is required.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

# Terraform arguments that hold GCP resource labels when the resource does not
# use a top-level `labels` map. Do not include Kubernetes node `node_config.labels`.
GCP_LABEL_ATTRIBUTE_ALIASES = (
    "resource_labels",
    "user_labels",
    "settings.user_labels",
    "settings.0.user_labels",
    "node_config.resource_labels",
    "node_config.0.resource_labels",
)

# Resources that accept labels under one of the aliases above. Kept next to the
# alias list so gcp_taggable and the solver stay in sync.
GCP_ALTERNATE_LABEL_RESOURCES = (
    "google_container_cluster",
    "google_container_node_pool",
    "google_monitoring_alert_policy",
    "google_monitoring_custom_service",
    "google_monitoring_group",
    "google_monitoring_service",
    "google_monitoring_slo",
    "google_monitoring_uptime_check_config",
    "google_sql_database_instance",
)


def _resource_type_name(vertex: Dict[str, Any]) -> str:
    resource_type = vertex.get("resource_type")
    if isinstance(resource_type, list) and resource_type:
        resource_type = resource_type[0]
    return resource_type if isinstance(resource_type, str) else ""


def _vertex_has_attribute(vertex: Dict[str, Any], path: str) -> bool:
    if vertex.get(path) is not None:
        return True
    prefix = f"{path}."
    return any(isinstance(key, str) and key.startswith(prefix) for key in vertex)


def resolve_gcp_label_attribute(vertex: Dict[str, Any], attribute: Optional[str]) -> Optional[str]:
    """Map policy attribute `labels` / `labels.*` to the GCP field this resource uses.

    Custom YAML policies typically check `attribute: labels` on `taggable` resources.
    Several GCP types store those maps as `resource_labels`, `user_labels`, or
    `settings.user_labels` instead. Leave non-GCP vertices and explicit alias
    attributes unchanged. Does not mutate solver state (solvers run concurrently).
    """
    if not attribute or (attribute != "labels" and not attribute.startswith("labels.")):
        return attribute
    if not _resource_type_name(vertex).startswith("google_"):
        return attribute
    if _vertex_has_attribute(vertex, "labels"):
        return attribute

    suffix = attribute[len("labels"):]
    for alias in GCP_LABEL_ATTRIBUTE_ALIASES:
        if _vertex_has_attribute(vertex, alias):
            return f"{alias}{suffix}"
    return attribute
