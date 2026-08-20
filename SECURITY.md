# Security Policy

## Supported Versions

Security fixes are handled on the latest published version of Dot Skill. Users should update to
the newest tag or reinstall the latest Codex plugin version when security-related changes are
released.

## Credential Handling

Dot Skill helper scripts read the Dot. API key from the local `DOT_API_KEY` environment variable.
The local MCP server uses the same environment variable. The plugin, server, and scripts do not
store API keys, device IDs, or request history.

Requests are sent to the Dot. OpenAPI service at:

```text
https://dot.mindreset.tech
```

## User Responsibilities

- Do not commit `.env`, API keys, device serial numbers, or private image URLs.
- Rotate your Dot. API key if it may have been exposed.
- Use separate API keys for development, demos, and production workflows when possible.
- Review generated Canvas, text, image, and link payloads before sending them to a real device.
- Keep the MCP process environment private. Do not pass `DOT_API_KEY` as a tool argument or place it
  in an MCP configuration file.

## Reporting a Vulnerability

Please follow the official Dot. responsible disclosure policy:

```text
https://dot.mindreset.tech/docs/security_policy
```

Submit security vulnerability reports by email:

```text
security@mindreset.tech
```

MindReset will acknowledge receipt within 24 hours and provide an initial response within 72 hours.
After a vulnerability is confirmed, the security team will fix it as quickly as possible and publish
a security advisory when appropriate.

Please include:

- A concise description of the issue
- Affected script, endpoint, or documentation section
- Reproduction steps when safe to share
- Any suggested mitigation

Do not include live API keys, real device IDs, or private user data in reports unless strictly
necessary for responsible validation. Please do not publicly disclose vulnerability details before
the issue is fixed.
