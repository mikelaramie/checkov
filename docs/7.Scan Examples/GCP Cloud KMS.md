---
layout: default
published: true
title: GCP Cloud KMS hardware-backed keys
nav_order: 25
---

# GCP Cloud KMS hardware-backed keys

`CKV_GCP_129` fails Terraform `google_kms_crypto_key` resources whose key material is not hardware-backed. The provider default protection level is `SOFTWARE`, which is not enough for FIPS / key-custody evidence that requires HSM.

Scan a directory of Terraform:

```shell
checkov -d . --check CKV_GCP_129 --framework terraform
```

## What passes

- `version_template.protection_level` is `HSM` (multi-tenant Cloud HSM)
- `version_template.protection_level` is `HSM_SINGLE_TENANT`
- `crypto_key_backend` points at a Single-tenant Cloud HSM instance (`…/singleTenantHsmInstances/…`)

```hcl
resource "google_kms_crypto_key" "pass_hsm" {
  name     = "pass-hsm"
  key_ring = google_kms_key_ring.keyring.id

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "HSM"
  }
}
```

## What fails

- No `version_template` (defaults to `SOFTWARE`)
- `version_template` without `protection_level`
- Explicit `SOFTWARE`
- Cloud EKM: `EXTERNAL`, `EXTERNAL_VPC`, or `crypto_key_backend` to `…/ekmConnections/…` (EKM backing is not visible as HSM in Terraform)

## How to fix

Set a hardware protection level on the crypto key. For single-tenant Cloud HSM, also set `crypto_key_backend` to the instance resource name, for example `projects/PROJECT/locations/LOCATION/singleTenantHsmInstances/INSTANCE`.

See [Cloud KMS protection levels](https://cloud.google.com/kms/docs/protection-levels) and the Terraform [`google_kms_crypto_key`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/kms_crypto_key) resource.

## Related checks

| ID | Coverage |
|----|----------|
| `CKV_GCP_129` | This check: GCP crypto keys are hardware-backed |
| `CKV_GCP_43` | GCP KMS key rotation |
| `CKV_GCP_82` | GCP KMS `lifecycle.prevent_destroy` |
| `CKV_GCP_112` | GCP KMS IAM is not public |
| `CKV_AZURE_112` | Azure Key Vault keys use `RSA-HSM` / `EC-HSM` |

AWS customer-managed keys are not covered by this check. Default AWS KMS CMKs vs CloudHSM custom key stores vs imported `EXTERNAL` origin is a separate mapping.
