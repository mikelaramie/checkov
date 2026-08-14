# Check ID allocation

Two independent counters per provider. Never mix them.

1. Grep the prefix you need, e.g. `CKV_GCP_` or `CKV2_GCP_`.
2. Take the **highest numeric suffix + 1**.
3. Do **not** fill holes. Retired IDs are skipped on purpose.

`tests/terraform/runner/test_runner.py` → `test_no_missing_ids` requires contiguous sequences except documented skips.

Known GCP Python skips (do not recreate):

- `CKV_GCP_5` — no longer a valid platform check
- `CKV_GCP_19` — deprecated GCP configuration
- `CKV_GCP_67` — no longer deployable

GCP graph (`CKV2_GCP_*`) currently has no skipped numbers; keep it contiguous.

Also:

- IDs must be unique (`test_check_ids_dont_collide`).
- Python `CKV_GCP_*` includes `data/gcp` checks, not only `resource/gcp`.
- If two people might land the same next ID, search open PRs / local branches before committing.
