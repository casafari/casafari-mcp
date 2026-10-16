#!/usr/bin/env bash
# Casafari API and MCP Platform, REST quick start.
# Key: CASAFARI_API_KEY (cf_sk_...), from https://platform.casafari.com/console/
# Endpoints checked against:
#   https://platform.casafari.com/v1/locations/openapi.json
#   https://platform.casafari.com/v1/comparables/openapi.json
#   https://platform.casafari.com/v1/claro/openapi.json
set -euo pipefail
BASE=https://platform.casafari.com
AUTH=(-H "Authorization: Bearer ${CASAFARI_API_KEY:-}")

echo "1. Location Lookup (free)"
curl -sS -w '\nHTTP %{http_code}\n' "${AUTH[@]}" "$BASE/v1/locations/search?query=Madrid&country=ES&size=3"

echo "2. Comparables: apartments for sale within 1 km of a point"
curl -sS -w '\nHTTP %{http_code}\n' "${AUTH[@]}" -X POST "$BASE/v1/comparables/search" \
  -H 'Content-Type: application/json' \
  -d '{"comparables_count":5,"operation":"sale","comparables_types":["apartment"],"bedrooms":2,
       "location_boundary":{"circle":{"distance":1,"target_point":{"coordinates":{"latitude":40.4168,"longitude":-3.7038}}}}}'

echo "3. Claro: commercial premises in Spain from a brief"
curl -sS -w '\nHTTP %{http_code}\n' "${AUTH[@]}" -X POST "$BASE/v1/claro/search?limit=5" \
  -H 'Content-Type: application/json' \
  -d '{"brief":"Burger restaurant in Madrid, ground floor, 120-250 m2, smoke outlet, rent under 8,000 a month"}'
