# Python vs graph

| Choose | When |
|---|---|
| Python `checks/resource/<provider>/` | Inspect attributes on **one** resource. Nested blocks, `dynamic`, regex, loops, or `UNKNOWN` for unresolved variables. |
| YAML `checks/graph_checks/<provider>/` | Require a **connection** (network ↔ firewall, project ↔ audit config). AND/OR across resource types. Also fine for simple "attribute exists/equals" if YAML is shorter. |

Python IDs: `CKV_<PROVIDER>_<N>` (shared across `resource/`, `data/`, `provider/` for that provider).

Graph IDs: `CKV2_<PROVIDER>_<N>` — separate sequence. The `2` means graph engine, not "v2 of a Python check."

Python helpers:

- `BaseResourceValueCheck` — key should equal an expected value (`get_inspected_key`)
- `BaseResourceNegativeValueCheck` — key must not be a forbidden value
- `BaseResourceCheck` — custom `scan_resource_conf`

YAML `cond_type`: `attribute`, `connection`, `filter`. Combine with `and` / `or` / `not`.

If the requirement is "resource A must have related resource B," it is a graph check. If it is "this bucket sets `uniform_bucket_level_access`," Python is the usual choice.
