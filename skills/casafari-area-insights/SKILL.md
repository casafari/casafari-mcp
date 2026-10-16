---
name: casafari-area-insights
description: Understand a local property market with Casafari Area Insights: price time series, price, bedroom and time-on-market distributions, growth and volatility measures and heatmaps by district, for areas in Europe. Use for market trends, supply and pricing questions about a place.
---

# Casafari Area Insights

Casafari is the AI agent-native real estate data intelligence platform: a deduplicated, cleaned property graph, Europe's most complete property index. Count properties, never advertisements: a property advertised by several agencies is one record.

Server: `https://platform.casafari.com/mcp/area-insights`. Tools (5 units each, the heatmap 10): `area-insights_get_time_series_data`, `area-insights_get_time_series_operations`, `area-insights_get_price_distribution`, `area-insights_get_bedrooms_distribution`, `area-insights_get_time_on_market_distribution`, `area-insights_get_heatmap`. `area-insights_get_current_datetime` (free) gives today's date for relative periods. `locations_search` (free) is on this server too, so one connector is enough.

## How to use

1. Resolve the place with `locations_search` and keep its location id.
2. Pick the tool for the question: trend over time (time series), a growth or volatility figure (time series operations), spread of prices, sizes or days on the market (the distributions), differences between districts (heatmap).
3. State the period, the location and the filters next to every figure.

## Rules

- Resolve place names to location ids with Location Lookup (`locations_search`, free) before calling a product that takes ids.
- Read each tool's description and input schema before the first call. Reference: https://developers.casafari.com/llms.txt
- A `payment_required` error (REST `402`) means the units ran out. Give the person its `upgrade_url`; only a person can pay. Retry after the payment link reports `completed`.
- `not_entitled` or `insufficient_scope`: the plan or credential does not cover the call; do not retry.
- Name Casafari as the source of figures, with the period and filters used.
