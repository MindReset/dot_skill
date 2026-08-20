# Agent support

Dot Skill gives compatible agents two reusable surfaces:

- Agent Skills under `skills/`, with one canonical `SKILL.md` per capability.
- A local stdio MCP server with the fixed tools documented in [`mcp-configs.md`](./mcp-configs.md).

The API key is read from `DOT_API_KEY` in the local process environment. Remote MCP is not part of this release.

## Status

`Supported` means the repository has an established native installation route. `MCP available` means the agent can use the local server through its MCP configuration. `Experimental` means the standard Skill or MCP route is included, but a platform-specific smoke test has not been completed in this repository.

| Agent | Status | Skill route | MCP route |
| --- | --- | --- | --- |
| Codex | Supported | Codex marketplace in `.agents/plugins/marketplace.json` | Portable `mcp.json` |
| Claude Code | Experimental | `.claude-plugin/plugin.json` and `skills/` | `.mcp.json` |
| CodeBuddy | Experimental | `.codebuddy-plugin/plugin.json` and `skills/` | `.mcp.json` |
| Cursor | Experimental | Standard `skills/` or `.agents/skills/` | Cursor MCP configuration |
| VS Code Copilot | Experimental | Agent Plugin or `.github/skills/` | `.vscode/mcp.json` |
| Kimi Code | Experimental | Standard `skills/` or `.agents/skills/` | `.kimi-code/mcp.json` |
| Hermes | Experimental | Standard Agent Skills | Local stdio MCP |
| OpenCode | Experimental | Standard Agent Skills | Local MCP server |
| Gemini CLI | Experimental | Standard Agent Skills | `gemini mcp add` |
| Goose | Experimental | Standard Agent Skills | Local stdio extension |
| Trae | Experimental | `.trae/skills/` | Trae MCP configuration |
| MiniMax Code | Experimental | Use the Skill route exposed by the installed version | MCP-first |
| DeepSeek Harness | Experimental | Standard Agent Skills | Local stdio MCP |
| OpenAI GPT Actions | Supported via OpenAPI | OpenAPI schema | OpenAPI import |

The following integrations are intentionally not included in this release: native DeepSeek Harness plugins, Remote MCP, MCP Registry publication, Cline, Roo Code, Windsurf, Zed, and JetBrains ACP adapters. They can be added after their extension contracts are stable enough to test.

## Shared installation

From a published or Git checkout, install the local server with either command:

```bash
pipx install git+https://github.com/MindReset/dot_skill.git
```

```bash
uvx --from git+https://github.com/MindReset/dot_skill.git dot-mcp
```

Set the credential in the same environment that starts the agent:

```bash
export DOT_API_KEY="dot_app_<your_api_key>"
```

Do not put the API key in a tool call, command argument, plugin manifest, or checked-in configuration file.
