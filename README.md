# Casafari MCP

**Property data intelligence, built for AI agents.**

Casafari is the AI agent-native real estate data intelligence platform. Deduplicated, cleaned property graph. Europe's most complete property index.

This repository holds configuration, skills and examples to connect AI agents to the Casafari API and MCP Platform: a Claude Code plugin and marketplace, a Cursor plugin, a Gemini CLI extension, copy-paste configs for other clients and REST examples. It contains no backend code and no keys.

The platform is self-serve: sign up at https://platform.casafari.com/console/ (Free plan, no card). One account, one key and one balance of units cover every product. When units run out, REST answers `402 payment_required` and MCP answers with a payment error, both with an `upgrade_url` a person opens to pay.

## The five MCP servers

Each server has a server card at `<url>/.well-known/mcp/server-card.json`. Tools are named `<server>_<tool>`, and every server also has `account_status`.

| Name | URL | What it does |
|---|---|---|
| `casafari-comparables` | `https://platform.casafari.com/mcp/comparables` | Comparable properties and price estimates for a subject property (`comparables_get-comparables`). |
| `casafari-area-insights` | `https://platform.casafari.com/mcp/area-insights` | Price series, price, bedroom and time-on-market distributions, growth and volatility, heatmaps by district. |
| `casafari-locations` | `https://platform.casafari.com/mcp/locations` | Find a place by name and get the location id every other product takes. Free. |
| `casafari-agentgraph` | `https://platform.casafari.com/mcp/agentgraph` | Real estate agencies and agents in Germany: screens, profiles, territory maps, partner briefs. Verified businesses only. |
| `casafari-claro` | `https://platform.casafari.com/mcp/claro` | Commercial premises across Spain and commercial plots in Germany, searched from a brief in plain words. |

MCP clients sign in with OAuth 2.1 in the browser: the server answers `401` with a `WWW-Authenticate` header that points to its protected-resource metadata, and a client discovers the rest from there. No key to copy. Unattended agents use a platform API key instead (`cf_sk_...`, as `Authorization: Bearer` or `X-API-Key`).

## Connect

Connect Location Lookup first; it is free and gives the ids the other products take. Docs for every client: https://developers.casafari.com/docs/connect.md

### Claude (claude.ai and desktop)

Settings, Connectors, add a custom connector, paste a server URL from the table (for example `https://platform.casafari.com/mcp/comparables`) and sign in. Repeat for each server you want.

### Claude Code

Install the plugin from this repository (all five servers and five skills):

```bash
claude plugin marketplace add casafari/casafari-mcp
claude plugin install casafari@casafari
```

Or add servers one by one, then run `/mcp` to sign in:

```bash
claude mcp add --transport http casafari-comparables https://platform.casafari.com/mcp/comparables
claude mcp add --transport http casafari-area-insights https://platform.casafari.com/mcp/area-insights
claude mcp add --transport http casafari-locations https://platform.casafari.com/mcp/locations
claude mcp add --transport http casafari-agentgraph https://platform.casafari.com/mcp/agentgraph
claude mcp add --transport http casafari-claro https://platform.casafari.com/mcp/claro
```

Docs: https://code.claude.com/docs/en/plugins and https://code.claude.com/docs/en/mcp

### Cursor

One-click install, one link per server (format from https://cursor.com/docs/mcp/install-links):

- [casafari-comparables](cursor://anysphere.cursor-deeplink/mcp/install?name=casafari-comparables&config=eyJ1cmwiOiJodHRwczovL3BsYXRmb3JtLmNhc2FmYXJpLmNvbS9tY3AvY29tcGFyYWJsZXMifQ==)
- [casafari-area-insights](cursor://anysphere.cursor-deeplink/mcp/install?name=casafari-area-insights&config=eyJ1cmwiOiJodHRwczovL3BsYXRmb3JtLmNhc2FmYXJpLmNvbS9tY3AvYXJlYS1pbnNpZ2h0cyJ9)
- [casafari-locations](cursor://anysphere.cursor-deeplink/mcp/install?name=casafari-locations&config=eyJ1cmwiOiJodHRwczovL3BsYXRmb3JtLmNhc2FmYXJpLmNvbS9tY3AvbG9jYXRpb25zIn0=)
- [casafari-agentgraph](cursor://anysphere.cursor-deeplink/mcp/install?name=casafari-agentgraph&config=eyJ1cmwiOiJodHRwczovL3BsYXRmb3JtLmNhc2FmYXJpLmNvbS9tY3AvYWdlbnRncmFwaCJ9)
- [casafari-claro](cursor://anysphere.cursor-deeplink/mcp/install?name=casafari-claro&config=eyJ1cmwiOiJodHRwczovL3BsYXRmb3JtLmNhc2FmYXJpLmNvbS9tY3AvY2xhcm8ifQ==)

Or put this in `~/.cursor/mcp.json` (or `.cursor/mcp.json` in a project), schema from https://cursor.com/docs/mcp:

```json
{
  "mcpServers": {
    "casafari-comparables": {
      "url": "https://platform.casafari.com/mcp/comparables"
    },
    "casafari-area-insights": {
      "url": "https://platform.casafari.com/mcp/area-insights"
    },
    "casafari-locations": {
      "url": "https://platform.casafari.com/mcp/locations"
    },
    "casafari-agentgraph": {
      "url": "https://platform.casafari.com/mcp/agentgraph"
    },
    "casafari-claro": {
      "url": "https://platform.casafari.com/mcp/claro"
    }
  }
}
```

This repository is also a Cursor plugin (`.cursor-plugin/plugin.json`, `mcp.json`, `skills/`), see https://cursor.com/docs/plugins.

### VS Code

`.vscode/mcp.json` (schema: https://code.visualstudio.com/docs/copilot/customization/mcp-servers):

```json
{
  "servers": {
    "casafari-comparables": {
      "type": "http",
      "url": "https://platform.casafari.com/mcp/comparables"
    },
    "casafari-area-insights": {
      "type": "http",
      "url": "https://platform.casafari.com/mcp/area-insights"
    },
    "casafari-locations": {
      "type": "http",
      "url": "https://platform.casafari.com/mcp/locations"
    },
    "casafari-agentgraph": {
      "type": "http",
      "url": "https://platform.casafari.com/mcp/agentgraph"
    },
    "casafari-claro": {
      "type": "http",
      "url": "https://platform.casafari.com/mcp/claro"
    }
  }
}
```

### ChatGPT

Turn on Developer mode in ChatGPT's settings (Apps and Connectors, advanced settings), create a connector, paste a server URL from the table as the MCP server URL, choose OAuth and sign in. Steps as published at https://developers.casafari.com/docs/connect.md.

### Gemini CLI

Install the extension (all five servers and `GEMINI.md`):

```bash
gemini extensions install https://github.com/casafari/casafari-mcp
```

Then run `/mcp auth casafari-comparables` (and the others) inside Gemini CLI. Or add servers one by one; the entry lands in `.gemini/settings.json` as `httpUrl`:

```bash
gemini mcp add --transport http casafari-comparables https://platform.casafari.com/mcp/comparables
gemini mcp add --transport http casafari-area-insights https://platform.casafari.com/mcp/area-insights
gemini mcp add --transport http casafari-locations https://platform.casafari.com/mcp/locations
gemini mcp add --transport http casafari-agentgraph https://platform.casafari.com/mcp/agentgraph
gemini mcp add --transport http casafari-claro https://platform.casafari.com/mcp/claro
```

Docs: https://github.com/google-gemini/gemini-cli/tree/main/docs/extensions

### Any other MCP client

Any client that supports remote MCP servers over Streamable HTTP with OAuth works: give it a server URL from the table.

## REST quick start

Base URL `https://platform.casafari.com/v1`, OpenAPI at https://platform.casafari.com/v1/openapi.json (one per product at `/v1/<product>/openapi.json`, Claro at https://platform.casafari.com/v1/claro/openapi.json). Send the key as `Authorization: Bearer` or `X-API-Key`, never in a query string.

```bash
export CASAFARI_API_KEY=cf_sk_...   # from https://platform.casafari.com/console/

# Location Lookup (free)
curl -H "Authorization: Bearer $CASAFARI_API_KEY" \
  "https://platform.casafari.com/v1/locations/search?query=Madrid&country=ES"

# Comparables
curl -X POST https://platform.casafari.com/v1/comparables/search \
  -H "Authorization: Bearer $CASAFARI_API_KEY" -H "Content-Type: application/json" \
  -d '{"operation":"sale","comparables_types":["apartment"],"comparables_count":5,
       "location_boundary":{"circle":{"distance":1,"target_point":{"coordinates":{"latitude":40.4168,"longitude":-3.7038}}}}}'
```

Full examples in [`examples/`](examples): [curl](examples/curl.sh), [Python](examples/python.py) and [TypeScript](examples/typescript.ts), each a Location Lookup, a Comparables call and a Claro search.

The existing Casafari API at api.casafari.com is for contract clients only; its tokens do not work on the platform.

## What is in this repository

| Path | For |
|---|---|
| `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.mcp.json`, `skills/` | Claude Code plugin and self-hosted marketplace |
| `.cursor-plugin/plugin.json`, `mcp.json`, `skills/` | Cursor plugin |
| `gemini-extension.json`, `GEMINI.md` | Gemini CLI extension |
| `examples/` | REST examples |

Skills: `casafari-comparables`, `casafari-area-insights`, `casafari-locations`, `casafari-agentgraph`, `casafari-claro`.

## Links

- Docs: https://developers.casafari.com (machine-readable: https://developers.casafari.com/llms.txt)
- Platform and console: https://platform.casafari.com
- Terms: https://developers.casafari.com/legal/platform-terms
- Contact: platform@casafari.com
- Security: see [SECURITY.md](SECURITY.md)

Licensed under the [Apache License 2.0](LICENSE).
