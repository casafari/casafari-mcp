"""Casafari REST quick start: Location Lookup, then Comparables, then Claro.

Key from the environment: CASAFARI_API_KEY (cf_sk_..., https://platform.casafari.com/console/).
Endpoints: platform.casafari.com/v1/locations/openapi.json,
           /v1/comparables/openapi.json, /v1/claro/openapi.json
"""
import json
import os

import requests

BASE = "https://platform.casafari.com"
KEY = os.environ["CASAFARI_API_KEY"]
HEADERS = {"Authorization": f"Bearer {KEY}"}


def call(method: str, path: str, **kw):
    r = requests.request(method, BASE + path, headers=HEADERS, timeout=60, **kw)
    if r.status_code == 402:  # units ran out: a person opens upgrade_url to pay
        raise SystemExit(f"payment_required: {r.json().get('upgrade_url')}")
    r.raise_for_status()
    return r.json()


# 1. Location Lookup (free): the location id other products take.
places = call("GET", "/v1/locations/search", params={"query": "Madrid", "country": "ES", "size": 3})
print(json.dumps(places, indent=2)[:800])

# 2. Comparables (20 units): apartments for sale within 1 km of a point.
comps = call("POST", "/v1/comparables/search", json={
    "comparables_count": 5,
    "operation": "sale",
    "comparables_types": ["apartment"],
    "bedrooms": 2,
    "location_boundary": {"circle": {
        "distance": 1,
        "target_point": {"coordinates": {"latitude": 40.4168, "longitude": -3.7038}},
    }},
})
print(json.dumps(comps, indent=2)[:800])

# 3. Claro (40 units): commercial premises in Spain from a brief in plain words.
claro = call("POST", "/v1/claro/search", params={"limit": 5}, json={
    "brief": "Burger restaurant in Madrid, ground floor, 120-250 m2, smoke outlet, rent under 8,000 a month",
})
print(json.dumps(claro, indent=2)[:800])
