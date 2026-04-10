# Dot Skill

**语言:** [English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja-JP.md)

用于 AI 助手通过 OpenAPI 与 Dot. 设备交互的 Skill。

📚 **官方文档**: [https://dot.mindreset.tech/docs/service/open/skill](https://dot.mindreset.tech/docs/service/open/skill)

## 什么是 Dot Skill？

Dot Skill 允许您：

- **控制设备内容**：在 Dot. 设备上显示文本、图像等内容
- **查询设备状态**：获取设备电池、WiFi 信号和当前显示内容的实时信息
- **管理设备**：列出您的设备、获取设备 ID、切换内容

## 前提条件

- 拥有一个 Dot. 账号和至少一台设备
- 从 Dot. App 获取 API 密钥
- 本地已安装 `python3`（用于使用辅助脚本）

## 安装

### 使用 `npx skills add` 安装（推荐）

```bash
npx skills add https://github.com/MindReset/dot_skill.git
```

仅安装此 skill：

```bash
npx skills add https://github.com/MindReset/dot_skill.git --skill dot-openapi
```

### 手动安装

```bash
mkdir -p ~/.agents/skills
ln -sfn /path/to/dot_skill/skills/dot-openapi ~/.agents/skills/dot-openapi
```

安装后请重启您的 agent。

## 快速开始

1. **获取 API 密钥**：按照[官方文档](https://dot.mindreset.tech/docs/service/open/get_api)操作
2. **获取设备 ID**：按照[官方文档](https://dot.mindreset.tech/docs/service/open/get_device_id)操作
3. **开始使用 API**：查看 [references/api_reference.md](skills/dot-openapi/references/api_reference.md) 了解所有可用接口

## API 概览

| 接口                                               | 方法 | 描述             |
| -------------------------------------------------- | ---- | ---------------- |
| `/api/authV2/open/devices`                         | GET  | 列出所有设备     |
| `/api/authV2/open/device/:deviceId/status`         | GET  | 获取设备状态     |
| `/api/authV2/open/device/:deviceId/next`           | POST | 切换到下一个内容 |
| `/api/authV2/open/device/:deviceId/text`           | POST | 显示文本内容     |
| `/api/authV2/open/device/:deviceId/image`          | POST | 显示图像内容     |
| `/api/authV2/open/device/:deviceId/:taskType/list` | GET  | 列出设备任务     |

## 辅助脚本

`scripts/` 目录包含 Python 辅助脚本：

- `send_text.py`：向设备发送文本
- `send_image.py`：向设备发送图像
- `get_device_status.py`：获取当前设备状态
- `list_devices.py`：列出所有设备

## 资源

- [API 参考](docs/api_reference.md) - 完整的 API 文档
- [认证指南](docs/authentication.md) - 如何认证请求
- [错误处理](docs/error_handling.md) - 常见错误和解决方案

## 许可证

MIT 许可证 - 详见 [LICENSE](./LICENSE)。
