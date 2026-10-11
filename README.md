# HypoPG — Windows x64 binaries (pgextwin)

[日本語](README_ja.md) | English

This repository publishes unofficial Windows x64 binaries of upstream [HypoPG](https://github.com/HypoPG/hypopg) **1.4.3**, pinned to commit `21d5461ad1868434cc47d9aa656d7afc2b24c464`.

**Current published release:** [v1.4.3-windows.1](https://github.com/pgextwin/hypopg/releases/tag/v1.4.3-windows.1), for PostgreSQL **14–18**. Download the ZIP matching your PostgreSQL major; the [pgextwin Catalog](https://pgextwin.github.io/website/en/) lists checksums, SPDX SBOMs, Grype reports and build attestations. This release is an independently built community distribution, not an official upstream Windows release.

The Windows CI verifies startup, `CREATE EXTENSION hypopg`, creation of a hypothetical index, the effect on an `EXPLAIN` plan without a physical index, and restoration after `hypopg_reset()`. Server-log assertions and extension upgrade paths are **not covered** by the current functional Test Contract. See the [pgextwin Catalog](https://pgextwin.github.io/website/en/) for the currently verified installation requirements and feature coverage.

HypoPG does not need shared preload for normal hypothetical-index use. PostgreSQL 14 is eligible for new builds through its official EOL of **2026-11-12**; existing published ZIPs remain available as historical assets after EOL. Confirm Windows PostgreSQL installation and ABI compatibility before production use.
