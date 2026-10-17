---
name: casafari-locations
description: Find a place by name with Casafari Location Lookup and get the location id every other Casafari product takes. Free. Use before any call that needs a location id, or to browse a place's parents and children.
---

# Casafari Location Lookup

Casafari is the AI agent-native real estate data intelligence platform: a deduplicated, cleaned property graph, Europe's most complete property index. Count properties, never advertisements: a property advertised by several agencies is one record.

Server: `https://platform.casafari.com/mcp/locations`. Tools (free): `locations_search`, `locations_get`. REST: `GET https://platform.casafari.com/v1/locations/search?query=Madrid&country=ES`, `GET /v1/locations/{location_id}`, `GET /v1/locations/{location_id}/children`, `GET /v1/locations/by-coordinates`.

## How to use

1. Search by name, with `country` (ISO code) to disambiguate.
2. If several places match, show them to the person or choose by the hierarchy and country; do not guess.
3. Pass the id to Area Insights or Comparables.

## Rules

- Resolve place names to location ids with Location Lookup (`locations_search`, free) before calling a product that takes ids.
- Read each tool's description and input schema before the first call. Reference: https://developers.casafari.com/llms.txt
- A `payment_required` error (REST `402`) means the units ran out. Give the person its `upgrade_url`; only a person can pay. Retry after the payment link reports `completed`.
- `not_entitled` or `insufficient_scope`: the plan or credential does not cover the call; do not retry.
- Name Casafari as the source of figures, with the period and filters used.
