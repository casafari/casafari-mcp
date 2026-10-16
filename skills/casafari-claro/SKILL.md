---
name: casafari-claro
description: Find commercial premises for rent or sale across Spain (shops, restaurant and cafe premises, gyms, offices, warehouses) and commercial plots in Germany from a brief in plain words, with Claro by Casafari: each premises checked criterion by criterion with the agency's own words as evidence. Use when a task needs premises that meet an expansion brief.
---

# Claro: commercial premises search

Casafari is the AI agent-native real estate data intelligence platform: a deduplicated, cleaned property graph, Europe's most complete property index. Count properties, never advertisements: a property advertised by several agencies is one record. Claro is Casafari's AI search for commercial premises: it checks every premises in the property graph against each criterion of a brief.

Server: `https://platform.casafari.com/mcp/claro`. REST: `https://platform.casafari.com/v1/claro` (OpenAPI https://platform.casafari.com/v1/claro/openapi.json). Premises cover all of Spain; plots cover Germany. Tools: `search_premises` (start here, 40 units), `refine_search`, `get_premises`, `compare_premises`, `market_snapshot`, `explain_location`, `brief_from_file`, `search_plots`, `get_plot`. The server card lists them with a `claro_` prefix.

## How to use

1. Send the brief as the person wrote it (`brief`), or `criteria` for exact filters. For a keyword-only search with no model, send `criteria.keywords` and `"check": false`.
2. Change a search with `refine_search`; open one result with `get_premises`; put 2 to 10 side by side with `compare_premises`. A brief file (PDF, Word, Excel, photo) goes through `brief_from_file`: show the person the brief and each requirement's quote and let them confirm before searching.
3. `market_snapshot` gives what premises of a kind ask in a place.

## Reporting rules

- Quote the evidence as given. A criterion marked `not_stated` means the description does not say; it never means the premises lacks it.
- Link a premises only to the URL the answer gives (the agency's own page). Never invent or reconstruct a link.
- Never name a private seller.
- Location Intelligence figures (footfall, spending power and the like) are indexes that compare places with each other, not head counts. Give each figure its meaning, unit and vintage as returned; never present a footfall index as people or visitors a day.
- Where the account has no location data access, the answer says so; do not fill the gap.
- Ids look like `pm_...`; they are the only ids to show or store.

## Rules

- Resolve place names to location ids with Location Lookup (`locations_search`, free) before calling a product that takes ids.
- Read each tool's description and input schema before the first call. Reference: https://developers.casafari.com/llms.txt
- A `payment_required` error (REST `402`) means the units ran out. Give the person its `upgrade_url`; only a person can pay. Retry after the payment link reports `completed`.
- `not_entitled` or `insufficient_scope`: the plan or credential does not cover the call; do not retry.
- Name Casafari as the source of figures, with the period and filters used.
