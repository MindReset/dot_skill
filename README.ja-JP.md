# Dot Skill

**言語:** [English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja-JP.md)

AI アシスタントが OpenAPI を通じて Dot. デバイスと連携するための Skill です。

📚 **公式ドキュメント**: [https://dot.mindreset.tech/docs/service/open/skill](https://dot.mindreset.tech/docs/service/open/skill)

## Dot Skill とは？

Dot Skill を使用すると、以下のことができます：

- **デバイスコンテンツの制御**: Dot. デバイスにテキスト、画像、Canvas API レイアウトなどのコンテンツを表示
- **Canvas レイアウトの設計**: 専用の Canvas designer skill で `windowData` カード、ダッシュボード、リスト、条件、フォーマットを作成
- **API コンテンツの命名**: テキスト、画像、Canvas API の内容にタスク別名を設定して一覧で見分けやすくする
- **デバイス状態の確認**: デバイスのバッテリー、WiFi 信号、現在の表示内容のリアルタイム情報を取得
- **デバイスの管理**: デバイスの一覧表示、デバイス ID の取得、コンテンツの切り替え

このリポジトリは役割を分けています：

- `dot-device-openapi`: デバイス操作、API 呼び出し、ヘルパースクリプト
- `dot-canvas-designer`: Canvas API `windowData` の設計とレイアウトガイド
- `dot-openapi`: 古いインストール向けの互換入口

## 前提条件

- Dot. アカウントと少なくとも 1 台のデバイス
- Dot. App から取得した API キー
- ローカルにインストールされた `python3`（ヘルパースクリプト使用時）

## インストール

### `npx skills add` でインストール（推奨）

```bash
npx skills add https://github.com/MindReset/dot_skill.git
```

デバイス操作 skill のみインストール：

```bash
npx skills add https://github.com/MindReset/dot_skill.git --skill dot-device-openapi
```

Canvas designer skill のみインストール：

```bash
npx skills add https://github.com/MindReset/dot_skill.git --skill dot-canvas-designer
```

### 手動インストール

```bash
mkdir -p ~/.agents/skills
ln -sfn /path/to/dot_skill/skills/dot-device-openapi ~/.agents/skills/dot-device-openapi
ln -sfn /path/to/dot_skill/skills/dot-canvas-designer ~/.agents/skills/dot-canvas-designer
```

インストール後、エージェントを再起動してください。

## クイックスタート

1. **API キーの取得**: [公式ドキュメント](https://dot.mindreset.tech/docs/service/open/get_api) を参照
2. **デバイス ID の取得**: [公式ドキュメント](https://dot.mindreset.tech/docs/service/open/get_device_id) を参照
3. **API の使用開始**: [Device API Reference](skills/dot-device-openapi/references/api_reference.md) でエンドポイントを確認し、[Canvas windowData Reference](skills/dot-canvas-designer/references/windowdata.md) で Canvas レイアウトを確認

## API 概要

| エンドポイント                                     | メソッド | 説明                       |
| -------------------------------------------------- | -------- | -------------------------- |
| `/api/authV2/open/devices`                         | GET      | すべてのデバイスを一覧表示 |
| `/api/authV2/open/timezones`                       | GET      | 対応タイムゾーンを一覧表示 |
| `/api/authV2/open/device/:deviceId/status`         | GET      | デバイス状態を取得         |
| `/api/authV2/open/device/:deviceId/settings`       | GET      | デバイス設定を取得         |
| `/api/authV2/open/device/:deviceId/settings`       | POST     | デバイス設定を更新         |
| `/api/authV2/open/device/:deviceId/next`           | POST     | 次のコンテンツに切り替え   |
| `/api/authV2/open/device/:deviceId/text`           | POST     | テキストコンテンツを表示   |
| `/api/authV2/open/device/:deviceId/image`          | POST     | 画像コンテンツを表示       |
| `/api/authV2/open/device/:deviceId/canvas`         | POST     | Canvas コンテンツを表示    |
| `/api/authV2/open/device/:deviceId/:taskType/list` | GET      | デバイスタスクを一覧表示   |

## ヘルパースクリプト

`skills/dot-device-openapi/scripts/` ディレクトリには Python ヘルパースクリプトが含まれています：

- `send_text.py`: デバイスにテキストを送信
- `send_image.py`: デバイスに画像を送信
- `send_canvas.py`: Canvas API の JSON レイアウトをデバイスに送信
- `get_device_status.py`: 現在のデバイス状態を取得
- `get_device_settings.py`: デバイス設定を取得
- `update_device_settings.py`: デバイス設定を更新
- `list_devices.py`: すべてのデバイスを一覧表示
- `list_tasks.py`: デバイスのループまたは固定タスクを一覧表示
- `switch_next.py`: 次のコンテンツに切り替え

テキスト、画像、Canvas のヘルパースクリプトは `--task-alias` に対応しており、デバイスのタスク一覧に表示される読みやすいタスク名を設定できます。

## リソース

- [Device API Reference](skills/dot-device-openapi/references/api_reference.md) - デバイス操作とエンドポイント
- [Canvas windowData Reference](skills/dot-canvas-designer/references/windowdata.md) - Canvas レイアウト設計ルール
- [Canvas Examples](skills/dot-canvas-designer/references/examples.md) - Canvas payload 例
- [認証ガイド](skills/dot-device-openapi/references/authentication.md) - リクエストの認証方法

## メンテナンスメモ

このリポジトリは、Dot. デバイス操作と Canvas 設計のための公開ユーザー向け skill package です。Dot Web の API 挙動を変更した場合は、次の項目も同期してください：

- `openapi/dot-openapi.yaml`：OpenAPI 互換 agent と GPT Actions 向け
- `skills/dot-device-openapi`：デバイス操作スクリプトとエンドポイント説明
- `skills/dot-canvas-designer`：Canvas API payload 設計ルール
- `plugins/dot-skill`：Codex plugin パッケージ内容
- `dot_web_docs` の Dot Web 公開ドキュメント

内部専用の Studio V2 実装、MongoDB migration、レンダー調査手順は `dot_internal_skill` に置き、この公開 package には含めないでください。

## ライセンス

MIT ライセンス - 詳細は [LICENSE](./LICENSE) を参照してください。
