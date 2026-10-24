# ChatGPT and Codex plugin packages

One folder per plugin, in OpenAI's portable layout (`plugin.json` with `extensions.com.openai.interface`, `mcp.json` with a `streamable-http` server and OAuth, `skills/`, `assets/`). The same package serves **ChatGPT and Codex**: OpenAI's plugin directory is shared by both, and Codex reads the root `plugin.json` (https://developers.openai.com/plugins/build/plugins). No `.codex-plugin/` folder is needed.

| Folder | Server | Coverage |
|---|---|---|
| `claro-ai` | `https://platform.casafari.com/mcp/claro` | Spain (premises), Germany (plots) |
| `casafari-comparables` | `https://platform.casafari.com/mcp/comparables` | 14 European countries |
| `casafari-area-insights` | `https://platform.casafari.com/mcp/area-insights` | 14 European countries |
| `casafari-location-lookup` | `https://platform.casafari.com/mcp/locations` | 14 European countries |

Each folder's `REVIEW.md` holds the submission form's test cases, negative cases and release notes; it is not part of the zip.

Build the zips (one per plugin, without `REVIEW.md`):

```bash
cd chatgpt && for p in */; do p=${p%/}; (cd "$p" && zip -qr "../$p.zip" . -x REVIEW.md); done
```

Rules: never name or link a property portal; never AgentGraph in a directory package; "properties", never "listings"; public text says "tokens".
