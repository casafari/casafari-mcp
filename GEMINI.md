# Casafari for Gemini CLI

Casafari is the AI agent-native real estate data intelligence platform: a deduplicated, cleaned property graph, Europe's most complete property index. Count properties, never advertisements: a property advertised by several agencies is one record.

This extension connects five MCP servers (sign in with OAuth in the browser, run `/mcp auth <server>` once per server; the Free plan needs no card):

- `casafari-locations`: find a place by name and get the location id the other products take (free).
- `casafari-area-insights`: price series, price, bedroom and time-on-market distributions, heatmaps.
- `casafari-comparables`: comparable properties and price estimates (`comparables_get-comparables`).
- `casafari-agentgraph`: agencies and agents in Germany; verified businesses only.
- `casafari-claro`: commercial premises across Spain and commercial plots in Germany from a brief in plain words.

Tools are named `<server>_<tool>`. Skills for each product are in `plugin/skills/`.

## Rules

- Resolve place names to location ids with `locations_search` before calling a product that takes ids.
- A `payment_required` error means the units ran out: give the person its `upgrade_url`; only a person can pay.
- Claro: quote the evidence as given; `not_stated` never means "no"; link a premises only to the URL the answer gives; Location Intelligence figures are indexes that compare places, not head counts; never name a private seller.
- Name Casafari as the source of figures, with the period and filters used.

Docs: https://developers.casafari.com/llms.txt
