from checkov.common.checks_infra.gcp_label_attributes import (
    GCP_ALTERNATE_LABEL_RESOURCES,
    resolve_gcp_label_attribute,
)
from checkov.common.checks_infra.resources_types import resources_types as raw_resources_types
from checkov.common.checks_infra.solvers.attribute_solvers.exists_attribute_solver import ExistsAttributeSolver


def test_gcp_taggable_includes_alternate_label_resources():
    gcp_taggable = raw_resources_types["gcp_taggable"]
    for resource_type in GCP_ALTERNATE_LABEL_RESOURCES:
        assert resource_type in gcp_taggable


def test_resolve_resource_labels():
    vertex = {
        "resource_type": "google_container_cluster",
        "resource_labels": {"env": "prod"},
        "resource_labels.env": "prod",
    }
    assert resolve_gcp_label_attribute(vertex, "labels") == "resource_labels"
    assert resolve_gcp_label_attribute(vertex, "labels.env") == "resource_labels.env"


def test_resolve_settings_user_labels():
    vertex = {
        "resource_type": "google_sql_database_instance",
        "settings.0.user_labels": {"env": "prod"},
        "settings.0.user_labels.env": "prod",
    }
    assert resolve_gcp_label_attribute(vertex, "labels") == "settings.0.user_labels"
    assert resolve_gcp_label_attribute(vertex, "labels.env") == "settings.0.user_labels.env"


def test_resolve_user_labels():
    vertex = {
        "resource_type": "google_monitoring_alert_policy",
        "user_labels": {"env": "prod"},
        "user_labels.env": "prod",
    }
    assert resolve_gcp_label_attribute(vertex, "labels") == "user_labels"


def test_resolve_prefers_existing_labels():
    vertex = {
        "resource_type": "google_storage_bucket",
        "labels": {"env": "prod"},
        "labels.env": "prod",
        "resource_labels": {"other": "value"},
    }
    assert resolve_gcp_label_attribute(vertex, "labels") == "labels"
    assert resolve_gcp_label_attribute(vertex, "labels.env") == "labels.env"


def test_resolve_ignores_kubernetes_node_config_labels():
    vertex = {
        "resource_type": "google_container_cluster",
        "node_config.0.labels": {"env": "prod"},
        "node_config.0.labels.env": "prod",
    }
    assert resolve_gcp_label_attribute(vertex, "labels") == "labels"
    assert resolve_gcp_label_attribute(vertex, "labels.env") == "labels.env"


def test_resolve_node_pool_resource_labels():
    vertex = {
        "resource_type": "google_container_node_pool",
        "node_config.0.resource_labels": {"env": "prod"},
        "node_config.0.resource_labels.env": "prod",
    }
    assert resolve_gcp_label_attribute(vertex, "labels") == "node_config.0.resource_labels"
    assert resolve_gcp_label_attribute(vertex, "labels.env") == "node_config.0.resource_labels.env"


def test_resolve_ignores_aws_and_explicit_alias_attributes():
    aws_vertex = {"resource_type": "aws_s3_bucket", "tags": {"env": "prod"}}
    assert resolve_gcp_label_attribute(aws_vertex, "tags.env") == "tags.env"
    gcp_vertex = {
        "resource_type": "google_container_cluster",
        "resource_labels": {"env": "prod"},
    }
    assert resolve_gcp_label_attribute(gcp_vertex, "resource_labels") == "resource_labels"


def test_exists_solver_treats_resource_labels_as_labels():
    solver = ExistsAttributeSolver(["google_container_cluster"], "labels", None)
    pass_vertex = {
        "resource_type": "google_container_cluster",
        "source_": "Terraform",
        "resource_labels": {"env": "prod"},
        "resource_labels.env": "prod",
    }
    fail_vertex = {
        "resource_type": "google_container_cluster",
        "source_": "Terraform",
    }
    assert solver.get_operation(pass_vertex) is True
    assert solver.get_operation(fail_vertex) is False


def test_exists_solver_treats_sql_user_labels_as_labels():
    solver = ExistsAttributeSolver(["google_sql_database_instance"], "labels.env", None)
    vertex = {
        "resource_type": "google_sql_database_instance",
        "source_": "Terraform",
        "settings.0.user_labels": {"env": "prod"},
        "settings.0.user_labels.env": "prod",
    }
    assert solver.get_operation(vertex) is True
