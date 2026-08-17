# Standard labels field (already on gcp_taggable)
resource "google_storage_bucket" "pass" {
  name     = "pass"
  location = "US"
  labels = {
    env = "prod"
  }
}

resource "google_storage_bucket" "fail" {
  name     = "fail"
  location = "US"
}

# GKE cluster: GCP labels are resource_labels, not labels
resource "google_container_cluster" "pass" {
  name = "pass"
  resource_labels = {
    env = "prod"
  }
}

resource "google_container_cluster" "fail" {
  name = "fail"
}

# Kubernetes node labels only — must not count as GCP resource labels
resource "google_container_cluster" "k8s_labels_only" {
  name = "k8s-labels-only"
  node_config {
    labels = {
      env = "prod"
    }
  }
}

# GKE node pool: GCP labels are node_config.resource_labels
resource "google_container_node_pool" "pass" {
  name    = "pass"
  cluster = "pass"
  node_config {
    resource_labels = {
      env = "prod"
    }
  }
}

resource "google_container_node_pool" "fail" {
  name    = "fail"
  cluster = "fail"
}

resource "google_container_node_pool" "k8s_labels_only" {
  name    = "k8s-labels-only"
  cluster = "fail"
  node_config {
    labels = {
      env = "prod"
    }
  }
}

# Cloud SQL: labels are settings.user_labels, not labels
resource "google_sql_database_instance" "pass" {
  name             = "pass"
  database_version = "POSTGRES_14"
  settings {
    tier = "db-f1-micro"
    user_labels = {
      env = "prod"
    }
  }
}

resource "google_sql_database_instance" "fail" {
  name             = "fail"
  database_version = "POSTGRES_14"
  settings {
    tier = "db-f1-micro"
  }
}

resource "google_monitoring_alert_policy" "pass" {
  display_name = "pass"
  combiner     = "OR"
  user_labels = {
    env = "prod"
  }
  conditions {
    display_name = "condition"
    condition_threshold {
      filter     = "metric.type=\"compute.googleapis.com/instance/cpu/utilization\""
      duration   = "60s"
      comparison = "COMPARISON_GT"
    }
  }
}

resource "google_monitoring_alert_policy" "fail" {
  display_name = "fail"
  combiner     = "OR"
  conditions {
    display_name = "condition"
    condition_threshold {
      filter     = "metric.type=\"compute.googleapis.com/instance/cpu/utilization\""
      duration   = "60s"
      comparison = "COMPARISON_GT"
    }
  }
}

# Not taggable — must not appear in pass/fail
resource "google_compute_network" "untagged" {
  name = "untagged"
}
