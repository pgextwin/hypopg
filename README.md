# HypoPG — Windows x64

[日本語](README_ja.md) | English

This repository provides **unofficial Windows x64 packages** of [HypoPG](https://github.com/HypoPG/hypopg). HypoPG lets you evaluate hypothetical indexes without creating physical indexes.

## Downloads and compatibility

Download the [latest published Release](https://github.com/pgextwin/hypopg/releases/latest), or [view all Releases](https://github.com/pgextwin/hypopg/releases). Published packages for PostgreSQL **14–18** are listed in the [pgextwin catalog](https://pgextwin.github.io/website/en/).

Select the ZIP for **your PostgreSQL major version**. Do not mix files built for different majors. PostgreSQL 14 community support ends on November 12, 2026; historical downloads may remain available afterward.

## Installation

1. Back up your installation and check the [upstream documentation](https://github.com/HypoPG/hypopg) for prerequisites.
2. Stop PostgreSQL before replacing installed files. Unpack the ZIP matching your PostgreSQL major.
3. Copy the packaged lib/ and share/extension/ files to the matching directories in your PostgreSQL installation.
4. Then create the extension in each database where it is needed using CREATE EXTENSION hypopg;. Normal hypothetical-index use does not require shared preloading. Restart PostgreSQL if you changed server configuration.

Check the Release's SHA256SUMS.txt against the downloaded ZIP. Other available release materials can include SPDX SBOMs, vulnerability reports and signed attestations. Test in a non-production environment before deployment.

## Upstream and license

For usage, settings and limitations, refer to [HypoPG upstream](https://github.com/HypoPG/hypopg). This independent package is not an official upstream Windows distribution. The included license notices govern redistribution.
