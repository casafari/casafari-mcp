---
name: casafari-agentgraph
description: Find and screen real estate agencies and agents in Germany with Casafari AgentGraph AI: area screens against partner profiles, full profiles, territory maps, partner briefs and watchlists. Verified businesses only. Use for agency partnership research in Germany.
---

# Casafari AgentGraph AI

Casafari is the AI agent-native real estate data intelligence platform: a deduplicated, cleaned property graph, Europe's most complete property index. Count properties, never advertisements: a property advertised by several agencies is one record.

Server: `https://platform.casafari.com/mcp/agentgraph`. Germany only. Only accounts of verified businesses can use it: a `verification_required` error means the business is not verified yet; tell the person and do not retry.

Tools: `agentgraph_find_location` (free, resolves a German place), `agentgraph_list_profiles` (free), `agentgraph_screen_agencies` and `agentgraph_screen_agents` (250 units), `agentgraph_agency_profile` and `agentgraph_agent_profile` (10), `agentgraph_territory_map` (20), `agentgraph_area_benchmark` (10), `agentgraph_partner_brief` (2,500), `agentgraph_save_to_watchlist` (5), `agentgraph_remove_from_watchlist`, `agentgraph_watchlist` (1), `agentgraph_watchlist_changes` (5).

## How to use

1. Resolve the place with `agentgraph_find_location` (this server has its own; do not use Location Lookup ids here).
2. List the partner profiles, then screen agencies or agents in the area against one profile.
3. Open a full profile only for the shortlisted ones; the partner brief is the costly call, so confirm with the person first.
4. Saving to the watchlist changes the account's data: do it only when asked.
5. Never name a private seller; AgentGraph covers businesses.

## Rules

- Resolve place names to location ids with Location Lookup (`locations_search`, free) before calling a product that takes ids.
- Read each tool's description and input schema before the first call. Reference: https://developers.casafari.com/llms.txt
- A `payment_required` error (REST `402`) means the units ran out. Give the person its `upgrade_url`; only a person can pay. Retry after the payment link reports `completed`.
- `not_entitled` or `insufficient_scope`: the plan or credential does not cover the call; do not retry.
- Name Casafari as the source of figures, with the period and filters used.
