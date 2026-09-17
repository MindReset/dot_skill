# Contributing to Dot Skill

We welcome improvements to skills, public examples, documentation, helper scripts, OpenAPI descriptions, and MCP integrations. Issues and pull requests may be written in English, Simplified Chinese, or Japanese. Use the repository templates and keep each PR focused on one problem.

For a new public tool or a breaking API change, open an issue to discuss the use case before implementing it. Small fixes and documentation improvements can go directly to a PR.

## Edit the canonical source

| Area | Source |
| --- | --- |
| Device operations and product routing | `skills/dot-device-openapi/` |
| Content planning and Canvas design | `skills/dot-canvas-designer/` |
| Compatibility router | `skills/dot-openapi/` |
| Shared Python client, validation, and MCP server | `dot_mcp/` |
| Public API schema | `openapi/dot-openapi.yaml` |
| Installation and integration guidance | `README.md`, language variants, and `docs/` |

Reuse existing clients, helpers, and public contracts. Hardware features do not establish cloud API support: keep firmware development, local display protocols, and Dot cloud operations distinct. Keep internal-only APIs, data, credentials, and administrative procedures out of this public package.

## Keep the plugin bundle aligned

`plugins/dot-skill/` mirrors canonical content for portable installation. Do not edit only that copy. After changing bundled files, run from the repository root:

```sh
python scripts/sync_bundle.py
```

The script also synchronizes compatibility helper scripts. Review its output and include the corresponding mirrored changes in the same PR. To inspect synchronization without changing files:

```sh
python scripts/sync_bundle.py --check
```

## Verification and compatibility

Describe the checks you actually performed and any remaining gaps. For documentation-only edits, review links, examples, and affected translations; a test run is not required. For runtime changes, provide a focused reproduction or check of the changed behavior. Identify affected agent platforms and installation methods when relevant.

Do not require contributors to send content to a physical device merely to fix documentation. Do not describe a live API or device behavior as verified unless you checked it. Keep secrets and personal content out of logs, payloads, and screenshots.

Update the schema and user documentation when a public interface changes. Add an `Unreleased` changelog entry for notable behavior changes; version bumps and release dates are handled as part of a release.

## Rights and communication

Submit material you have the right to share under the repository's [MIT license](LICENSE). Preserve third-party attribution and applicable license notices. Keep discussions respectful, specific, and focused on the contribution.

Use [Support](SUPPORT.md) for help and scope questions. Follow [Security](SECURITY.md) to report vulnerabilities privately.
