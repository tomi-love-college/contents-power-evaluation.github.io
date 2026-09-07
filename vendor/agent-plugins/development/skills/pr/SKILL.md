---
name: pr
description: 作業ブランチを push し、Summary と Test plan 付きの PR を作成する。
---

# プルリクエスト

この Skill は GitHub 上の PR 作成手順だけを持つ。デプロイ権限や会社の可変データは持たない。

## 手順

1. 未コミット変更が残っていないことを確認する。
2. 作業ブランチを remote へ push する。force push はしない。
3. PR 本文に **Summary** と **Test plan** を書く。UI 変更があれば確認方法も書く。
4. `gh pr create` で作成する。既存作業ブランチへ直接載せない。
5. PR open / synchronize で staging や production が起動する workflow がある場合は作成しない。

## やってはいけないこと

- `/deploy` コメント、production タグ、本番 workflow の起動
- 秘密情報や個人パスを PR 本文へ貼る
- マージやデプロイをこの Skill だけで完了扱いにする
