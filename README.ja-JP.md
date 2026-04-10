# Dot Skill

**言語:** [English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja-JP.md)

AI アシスタントが OpenAPI を通じて Dot. デバイスと連携するための Skill です。

📚 **公式ドキュメント**: [https://dot.mindreset.tech/docs/service/open/skill](https://dot.mindreset.tech/docs/service/open/skill)

## Dot Skill とは？

Dot Skill を使用すると、以下のことができます：

- **デバイスコンテンツの制御**: Dot. デバイスにテキスト、画像などのコンテンツを表示
- **デバイス状態の確認**: デバイスのバッテリー、WiFi 信号、現在の表示内容のリアルタイム情報を取得
- **デバイスの管理**: デバイスの一覧表示、デバイス ID の取得、コンテンツの切り替え

## 前提条件

- Dot. アカウントと少なくとも 1 台のデバイス
- Dot. App から取得した API キー
- ローカルにインストールされた `python3`（ヘルパースクリプト使用時）

## インストール

### `npx skills add` でインストール（推奨）

```bash
npx skills add https://github.com/MindReset/dot_skill.git
```

この skill のみインストール：

```bash
npx skills add https://github.com/MindReset/dot_skill.git --skill dot-openapi
```

### 手動インストール

```bash
mkdir -p ~/.agents/skills
ln -sfn /path/to/dot_skill/skills/dot-openapi ~/.agents/skills/dot-openapi
```

インストール後、エージェントを再起動してください。

## クイックスタート

1. **API キーの取得**: [公式ドキュメント](https://dot.mindreset.tech/docs/service/open/get_api) を参照
2. **デバイス ID の取得**: [公式ドキュメント](https://dot.mindreset.tech/docs/service/open/get_device_id) を参照
3. **API の使用開始**: [references/api_reference.md](skills/dot-openapi/references/api_reference.md) で利用可能なエンドポイントを確認

## API 概要

| エンドポイント                                     | メソッド | 説明                       |
| -------------------------------------------------- | -------- | -------------------------- |
| `/api/authV2/open/devices`                         | GET      | すべてのデバイスを一覧表示 |
| `/api/authV2/open/device/:deviceId/status`         | GET      | デバイス状態を取得         |
| `/api/authV2/open/device/:deviceId/next`           | POST     | 次のコンテンツに切り替え   |
| `/api/authV2/open/device/:deviceId/text`           | POST     | テキストコンテンツを表示   |
| `/api/authV2/open/device/:deviceId/image`          | POST     | 画像コンテンツを表示       |
| `/api/authV2/open/device/:deviceId/:taskType/list` | GET      | デバイスタスクを一覧表示   |

## ヘルパースクリプト

`scripts/` ディレクトリには Python ヘルパースクリプトが含まれています：

- `send_text.py`: デバイスにテキストを送信
- `send_image.py`: デバイスに画像を送信
- `get_device_status.py`: 現在のデバイス状態を取得
- `list_devices.py`: すべてのデバイスを一覧表示

## リソース

- [API リファレンス](skills/dot-openapi/references/api_reference.md) - 完全な API ドキュメント
- [認証ガイド](skills/dot-openapi/references/authentication.md) - リクエストの認証方法

## ライセンス

MIT ライセンス - 詳細は [LICENSE](./LICENSE) を参照してください。
