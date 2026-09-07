# Agent Plugins 利用設定（このリポジトリ）

このリポジトリは単独 clone で Plugin 定義を読める。親 workspace や社内 catalog は不要。
認証情報、会社の可変データ、個人ホームの設定はここへ置かない。

## 配置

| パス | 役割 |
|---|---|
| `gurade.agent-project.json` | 利用する Plugin と要求 component。ぐらで独自形式 |
| `gurade.agent-project.lock.json` | 内容 digest と adapter 版の固定 |
| `vendor/agent-plugins/development` | 公開可能な共通開発 Plugin の固定 snapshot |

このリポに固有開発手順の Skill は無い。空の `agent-plugins/` は置かない。
標準ファイルは各 Plugin の `plugin.json` / `skills/` だけ。独自フィールドを標準 manifest へ足さない。

## 確認

リポジトリルートで:

```sh
python3 tools/agent-setup/check.py
```

`agent-platform` が `PYTHONPATH` またはインストール済みなら、同じディレクトリで lock の完全照合も行う。

```sh
PYTHONPATH=/path/to/agent-platform/src python3 -m agent_platform.cli verify-lock
PYTHONPATH=/path/to/agent-platform/src python3 -m agent_platform.cli doctor --client claude
```

`/path/to/agent-platform` は利用者が持っているローカル checkout を指す。このリポジトリは親 workspace の固定パスを埋め込まない。toolchain が無い環境でも `check.py` のローカル検査は通る。

## 認証

この利用設定に MCP は無い。認証不足で外部送信や本番操作へ進まない。
native client への自動インストールは行わない。`doctor` は review 出力まで。

## 既存フロー

`index.html` と `content-power-analysis.md` の現行サイト本文は残す。
今回追加した Plugin は並行配置であり、切替（物理移動）は後続工程。
