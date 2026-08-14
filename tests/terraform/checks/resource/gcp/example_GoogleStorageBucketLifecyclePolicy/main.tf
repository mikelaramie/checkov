# SHOULD PASS: archives at 180 days, no early delete
resource "google_storage_bucket" "pass" {
  name     = "pass"
  location = "US"

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
    condition {
      age = 180
    }
  }
}

# SHOULD PASS: archives after 180 days and deletes only after 365
resource "google_storage_bucket" "pass_with_delete" {
  name     = "pass-with-delete"
  location = "US"

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
    condition {
      age = 200
    }
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 365
    }
  }
}

# SHOULD FAIL: no lifecycle policy
resource "google_storage_bucket" "fail_missing" {
  name     = "fail-missing"
  location = "US"
}

# SHOULD FAIL: archives too early
resource "google_storage_bucket" "fail_archive_too_soon" {
  name     = "fail-archive-too-soon"
  location = "US"

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
    condition {
      age = 90
    }
  }
}

# SHOULD FAIL: deletes before 90 days
resource "google_storage_bucket" "fail_early_delete" {
  name     = "fail-early-delete"
  location = "US"

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
    condition {
      age = 180
    }
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }
}

# SHOULD FAIL: lifecycle exists but never moves to Archive
resource "google_storage_bucket" "fail_no_archive" {
  name     = "fail-no-archive"
  location = "US"

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 365
    }
  }
}

# SHOULD FAIL: Coldline is not Archive storage
resource "google_storage_bucket" "fail_coldline" {
  name     = "fail-coldline"
  location = "US"

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
    condition {
      age = 180
    }
  }
}
