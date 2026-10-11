# HypoPG — Windows x64 バイナリ（pgextwin）

[English](README.md) | 日本語

上流 [HypoPG](https://github.com/HypoPG/hypopg) **1.4.3**（固定コミット `21d5461ad1868434cc47d9aa656d7afc2b24c464`）を基にした、非公式のWindows x64向けコミュニティ製バイナリです。

**現在の公開Release：** [v1.4.3-windows.1](https://github.com/pgextwin/hypopg/releases/tag/v1.4.3-windows.1)。PostgreSQL **14〜18**向けの各ZIPを公開しています。使用中のPGメジャーに対応するZIPを選んでください。SHA256・SPDX SBOM・Grype・ビルド証明は[pgextwin Pages](https://pgextwin.github.io/website/ja/)で確認できます。上流公式によるWindows配布ではありません。

Windows CIではPostgreSQL起動、`CREATE EXTENSION hypopg`、仮想インデックスによる`EXPLAIN`の変化、物理インデックスが作成されないこと、および`hypopg_reset()`後の復帰を検証しています。**サーバーログ検証および拡張機能のアップグレードは現行の機能テスト対象外**です。詳細は[Windows導入・検証ガイド](docs/windows_ja.md)を参照してください。

通常の仮想インデックス機能に`shared_preload_libraries`は不要です。PostgreSQL 14の新規ビルド対象期間は公式EOLの**2026-11-12**までとし、公開済み成果物はEOL後も履歴として残します。実運用前に使用するWindows版PostgreSQLとの互換性を確認してください。
