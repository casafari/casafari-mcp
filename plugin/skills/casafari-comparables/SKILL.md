---
name: casafari-comparables
description: Value a property and find comparable properties with Casafari: comparable properties on the market, past sales and rentals, and official registry records around a point, an address or a cadastral reference, with price estimates. Use for valuation, comp analysis and fair-price checks in Europe.
---

# Casafari Comparables

Casafari is the AI agent-native real estate data intelligence platform: a deduplicated, cleaned property graph, Europe's most complete property index. Count properties, never advertisements: a property advertised by several agencies is one record.

Server: `https://platform.casafari.com/mcp/comparables`. Tool: `comparables_get_comparables`. REST: `POST https://platform.casafari.com/v1/comparables/search` takes the same search.

## How to use

1. Get the subject's point: coordinates, an address or (Spain) a cadastral reference. A circle (`location_boundary.circle` with `target_point` and `distance` in km, 0.05 to 50) or a closed polygon bounds the search.
2. Set `operation` (`sale` or `rent`) and `comparables_types` (for example `apartment`, `house`, `retail`, `office`).
3. For commercial types (`retail`, `office`, `warehouse`, `restaurant` and others), `total_area` in square metres is required unless a cadastral reference is given.
4. Tight radius (0.5 to 1 km) in cities, wider (2 to 5 km) in rural areas. Add `sold_or_rented_after` for past sales and rentals.
5. Report the estimate range together with the comparables behind it, the radius and the filters.

## Rules

- Resolve place names to location ids with Location Lookup (`locations_search`, free) before calling a product that takes ids.
- Read each tool's description and input schema before the first call. Reference: https://developers.casafari.com/llms.txt
- A `payment_required` error (REST `402`) means the units ran out. Give the person its `upgrade_url`; only a person can pay. Retry after the payment link reports `completed`.
- `not_entitled` or `insufficient_scope`: the plan or credential does not cover the call; do not retry.
- Name Casafari as the source of figures, with the period and filters used.
