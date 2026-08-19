resource "google_kms_key_ring" "keyring" {
  name     = "keyring-example"
  location = "us-central1"
}

resource "google_kms_crypto_key" "pass_hsm" {
  name     = "pass-hsm"
  key_ring = google_kms_key_ring.keyring.id
  purpose  = "ENCRYPT_DECRYPT"

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "HSM"
  }
}

resource "google_kms_crypto_key" "pass_hsm_single_tenant" {
  name     = "pass-hsm-single-tenant"
  key_ring = google_kms_key_ring.keyring.id
  purpose  = "ENCRYPT_DECRYPT"

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "HSM_SINGLE_TENANT"
  }
}

resource "google_kms_crypto_key" "pass_single_tenant_backend" {
  name               = "pass-single-tenant-backend"
  key_ring           = google_kms_key_ring.keyring.id
  purpose            = "ENCRYPT_DECRYPT"
  crypto_key_backend = "projects/example/locations/us-central1/singleTenantHsmInstances/hsm-1"
}

resource "google_kms_crypto_key" "fail_default" {
  name     = "fail-default"
  key_ring = google_kms_key_ring.keyring.id
}

resource "google_kms_crypto_key" "fail_software" {
  name     = "fail-software"
  key_ring = google_kms_key_ring.keyring.id

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "SOFTWARE"
  }
}

resource "google_kms_crypto_key" "fail_omit_protection_level" {
  name     = "fail-omit-protection-level"
  key_ring = google_kms_key_ring.keyring.id

  version_template {
    algorithm = "GOOGLE_SYMMETRIC_ENCRYPTION"
  }
}

resource "google_kms_crypto_key" "fail_external" {
  name     = "fail-external"
  key_ring = google_kms_key_ring.keyring.id

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "EXTERNAL"
  }
}

resource "google_kms_crypto_key" "fail_external_vpc" {
  name               = "fail-external-vpc"
  key_ring           = google_kms_key_ring.keyring.id
  crypto_key_backend = "projects/example/locations/us-central1/ekmConnections/ekm-conn"

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "EXTERNAL_VPC"
  }
}
