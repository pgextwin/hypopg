# HypoPG — Windows x64 バイナリ

[English](README.md) | 日本語

[HypoPG](https://github.com/HypoPG/hypopg)の**非公式Windows x64バイナリ**を配布しています。仮想インデックスを作成し、実際のインデックスを追加せずに実行計画を検討できます。

## ダウンロードと対応環境

[最新の公開Release](https://github.com/pgextwin/hypopg/releases/latest)からダウンロードできます。[過去のReleases](https://github.com/pgextwin/hypopg/releases)も確認できます。PostgreSQL **14〜18**向けの公開状況は[pgextwinカタログ](https://pgextwin.github.io/website/ja/)に掲載しています。

**利用中のPostgreSQLメジャーバージョンに一致するZIP**を選んでください。異なるメジャー向けのファイルは混在させないでください。PostgreSQL 14は2026年11月12日にコミュニティサポートが終了します。過去の配布ファイルはその後も残る場合があります。

## インストール

1. 事前にバックアップを取り、[上流ドキュメント](https://github.com/HypoPG/hypopg)で必要な環境を確認します。
2. 既存ファイルの入れ替え前にPostgreSQLを停止し、対応するZIPを展開します。
3. ZIP内のlib/とshare/extension/のファイルを、PostgreSQLの同名ディレクトリへ配置してください。
4. 利用するデータベースでCREATE EXTENSION hypopg;を実行します。 通常の仮想インデックス利用には共有ライブラリの事前ロードは必要ありません。 サーバー設定を変更した場合はPostgreSQLを再起動します。

ダウンロードしたZIPはReleaseのSHA256SUMS.txtで照合できます。ReleaseによってはSPDX形式のSBOM、脆弱性レポート、署名付き証明も提供されています。本番環境の前に検証環境で動作を確認してください。

## 上流プロジェクトとライセンス

使い方、設定、制限事項は[上流のHypoPG](https://github.com/HypoPG/hypopg)を参照してください。本配布は上流の公式Windows版ではありません。再配布条件は同梱のライセンス表記に従います。
