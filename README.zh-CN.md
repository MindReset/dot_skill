# Dot Skill

**语言:** [English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja-JP.md)

![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-black)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-blue)
![MCP Ready](https://img.shields.io/badge/MCP-ready-blueviolet)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

用于 AI 助手通过 OpenAPI 与 Dot. 设备交互的 Skill。

📚 **官方文档**: [https://dot.mindreset.tech/docs/service/open/skill](https://dot.mindreset.tech/docs/service/open/skill)

## 什么是 Dot Skill？

Dot Skill 允许您：

- **控制设备内容**：在 Dot. 设备上显示文本、图像、画板 API 布局等内容
- **命名 API 内容**：为文本、图像和画板 API 内容设置任务别名，方便在任务列表中区分
- **查询设备状态**：获取设备电池、WiFi 信号和当前显示内容的实时信息
- **管理设备**：列出您的设备、获取设备 ID、切换内容

## 前提条件

- 拥有一个 Dot. 账号和至少一台设备
- 从 Dot. App 获取 API 密钥
- 本地已安装 `python3`（用于使用辅助脚本）

## 安装

### 作为 Codex 插件安装

将此仓库添加为 Codex marketplace：

```bash
codex plugin marketplace add git@github.com:MindReset/dot_skill.git
```

然后安装插件：

```bash
codex plugin add dot-skill@mindreset-dot-skill
```

安装后请新建一个 Codex 线程，以便 Codex 加载插件中的 skills。

### 用于 GPT Actions 或兼容 OpenAPI 的 agent

导入 OpenAPI schema：

```text
https://raw.githubusercontent.com/MindReset/dot_skill/master/openapi/dot-openapi.yaml
```

配置 Bearer 认证，使用 Dot. API key：

```http
Authorization: Bearer dot_app_<your_api_key>
```

公开 GPT 或会调用 Dot. API 的 agent 应包含 Dot. 隐私政策和用户协议：

- 隐私政策：[https://dot.mindreset.tech/docs/privacy](https://dot.mindreset.tech/docs/privacy)
- 用户协议：[https://dot.mindreset.tech/docs/terms](https://dot.mindreset.tech/docs/terms)

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

## Agent 平台兼容性

| 平台 | 状态 | 集成方式 |
| --- | --- | --- |
| Codex | 已支持 | 使用 `.agents/plugins/marketplace.json` 作为仓库 marketplace |
| OpenAI GPT Actions | 通过 schema 支持 | 导入 `openapi/dot-openapi.yaml` 并配置 Bearer 认证 |
| Claude / MCP clients | 计划中 | 目前可先使用 OpenAPI schema，后续可补 remote MCP server |
| Cursor 和兼容 skill 的 agent | 已支持为 skill 文档 | 安装 `skills/dot-openapi` 或将本仓库作为上下文 |
| MCP Registry | 计划中 | 等 Dot MCP server 存在后发布 server metadata |

## API 概览

| 接口                                               | 方法 | 描述             |
| -------------------------------------------------- | ---- | ---------------- |
| `/api/authV2/open/devices`                         | GET  | 列出所有设备     |
| `/api/authV2/open/device/:deviceId/status`         | GET  | 获取设备状态     |
| `/api/authV2/open/device/:deviceId/next`           | POST | 切换到下一个内容 |
| `/api/authV2/open/device/:deviceId/text`           | POST | 显示文本内容     |
| `/api/authV2/open/device/:deviceId/image`          | POST | 显示图像内容     |
| `/api/authV2/open/device/:deviceId/canvas`         | POST | 显示画板内容     |
| `/api/authV2/open/device/:deviceId/:taskType/list` | GET  | 列出设备任务     |

## 辅助脚本

`scripts/` 目录包含 Python 辅助脚本：

- `send_text.py`：向设备发送文本
- `send_image.py`：向设备发送图像
- `send_canvas.py`：向设备发送画板 API JSON 布局
- `get_device_status.py`：获取当前设备状态
- `list_devices.py`：列出所有设备
- `list_tasks.py`：列出设备循环或固定任务
- `switch_next.py`：切换到下一个内容

文本、图像和画板辅助脚本都支持 `--task-alias`，用于设置设备任务列表中显示的可读任务名称。

## 资源

- [API 参考](skills/dot-openapi/references/api_reference.md) - 完整的 API 文档
- [认证指南](skills/dot-openapi/references/authentication.md) - 如何认证请求
- [OpenAPI Schema](openapi/dot-openapi.yaml) - 可导入 Actions 和兼容 OpenAPI 的工具
- [安全政策](SECURITY.md) - 密钥处理和漏洞报告
- [Dot. 官方安全政策](https://dot.mindreset.tech/docs/security_policy) - 负责任披露流程
- [支持说明](SUPPORT.md) - Issue 提交指南
- [更新日志](CHANGELOG.md) - 发布记录

## 许可证

MIT 许可证 - 详见 [LICENSE](./LICENSE)。
