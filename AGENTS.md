# AGENTS.md

コンテンツ力診断（静的 GitHub Pages）の作業ルールです。
公開リポは `tomi-love-college/contents-power-evaluation.github.io`。サイト本文は [index.html](index.html) と [content-power-analysis.md](content-power-analysis.md) を正本にする。

## 常時制約

- 公開リポ。秘密情報、会社非公開 Plugin、社内 catalog 必須依存を置かない。
- GitHub Pages は `main` のルートから legacy デプロイする。PR open/sync では起動しない。
- エージェントから main へマージしない。merge は Pages をデプロイする。
- 本番相当の外部送信はしない。

## Agent Plugins

共通開発 Plugin の利用設定は [docs/agent-plugins.md](docs/agent-plugins.md)。
会社 Plugin は必須依存にしない。固有 Skill が無いので空の `agent-plugins/` は置かない。
利用設定はリポ内完結とし、親 workspace を前提にしない。
