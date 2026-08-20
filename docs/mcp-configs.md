# MCP configuration

The local server lets an MCP-capable agent list and control Dot. devices without exposing a generic HTTP client. It uses stdio and inherits `DOT_API_KEY` from the process environment.

## Common command

The Git-based command works without a separate checkout:

```text
command: uvx
args: ["--from", "git+https://github.com/MindReset/dot_skill.git", "dot-mcp"]
```

After `pipx install git+https://github.com/MindReset/dot_skill.git`, the shorter command is:

```text
command: dot-mcp
args: []
```

The repository root includes `plugin.json` and `mcp.json` for portable Agent Plugin consumers. Claude Code also uses the included `.claude-plugin/plugin.json` and `.mcp.json`; CodeBuddy uses `.codebuddy-plugin/plugin.json` and the same stdio shape.

## Claude Code, CodeBuddy, Cursor, and Kimi Code

Use the following `mcpServers` object in the platform's project MCP configuration. The exact file location is platform-specific; the repository includes the Claude-compatible `.mcp.json` form.

```json
{
  "mcpServers": {
    "dot-skill": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/MindReset/dot_skill.git",
        "dot-mcp"
      ]
    }
  }
}
```

Skill installation can use the repository's canonical `skills/` directory. For projects that require a discovery directory, copy or link the relevant skill directories into the platform's documented location:

- Claude Code: `skills/` or `.claude/skills/`
- CodeBuddy: `skills/` or `.codebuddy/skills/`
- Cursor: `skills/`, `.agents/skills/`, or `.cursor/skills/`
- Kimi Code: `skills/` or `.agents/skills/`

## VS Code Copilot

For a project-level `.vscode/mcp.json`, use the VS Code `servers` shape:

```json
{
  "servers": {
    "dot-skill": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/MindReset/dot_skill.git",
        "dot-mcp"
      ]
    }
  }
}
```

VS Code can discover the canonical skills through an Agent Plugin or a project skill directory such as `.github/skills/`. The repository's root `plugin.json` and `mcp.json` are the portable plugin entry points.

## OpenCode

Add a local MCP entry to the OpenCode configuration:

```json
{
  "mcp": {
    "dot-skill": {
      "type": "local",
      "command": [
        "uvx",
        "--from",
        "git+https://github.com/MindReset/dot_skill.git",
        "dot-mcp"
      ],
      "enabled": true
    }
  }
}
```

## Gemini CLI

Register the stdio command with the CLI:

```bash
gemini mcp add dot-skill -- uvx --from git+https://github.com/MindReset/dot_skill.git dot-mcp
```

## Hermes, Goose, and Trae

Create a local stdio extension using the platform's documented configuration format and use the common command above. The executable must inherit:

```text
DOT_API_KEY=dot_app_<your_api_key>
```

Trae can additionally discover the canonical skill by placing `dot-device-openapi` and `dot-canvas-designer` under `.trae/skills/`.

## MiniMax Code and DeepSeek Harness

Use MCP as the stable integration path for both platforms in this release. Configure a local stdio server with the common command above and keep the API key in the process environment. Do not depend on a native DeepSeek Harness plugin API; that surface is still developer preview. For MiniMax Code, the exact Skill discovery directory depends on the installed version, so MCP is the portable path.

## Tools and side effects

Read-only tools:

- `dot_list_devices`
- `dot_get_device_status`
- `dot_get_device_settings`
- `dot_list_timezones`
- `dot_list_tasks`
- `dot_validate_canvas`

Device-changing tools:

- `dot_update_device_settings`
- `dot_switch_next_content`
- `dot_send_text`
- `dot_send_image`
- `dot_send_canvas`

Write requests are not automatically retried. Text, image, and Canvas requests require a matching API content item in the device's loop task. `dot_validate_canvas` performs the shared local Canvas checks without contacting the service.
