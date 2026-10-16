// Casafari REST quick start: Location Lookup, then Comparables, then Claro.
// Key from the environment: CASAFARI_API_KEY (cf_sk_..., https://platform.casafari.com/console/).
// Run with Node 22+: node --experimental-strip-types examples/typescript.ts
// Endpoints: platform.casafari.com/v1/locations/openapi.json,
//            /v1/comparables/openapi.json, /v1/claro/openapi.json
const BASE = "https://platform.casafari.com";
const KEY = process.env.CASAFARI_API_KEY;
if (!KEY) throw new Error("Set CASAFARI_API_KEY");

async function call(method: string, path: string, body?: unknown): Promise<unknown> {
  const res = await fetch(BASE + path, {
    method,
    headers: { Authorization: `Bearer ${KEY}`, "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = await res.json();
  if (res.status === 402) throw new Error(`payment_required: ${(data as any).upgrade_url}`);
  if (!res.ok) throw new Error(`${res.status} ${JSON.stringify(data)}`);
  return data;
}

// 1. Location Lookup (free)
const places = await call("GET", "/v1/locations/search?query=Madrid&country=ES&size=3");
console.log(JSON.stringify(places, null, 2).slice(0, 800));

// 2. Comparables: apartments for sale within 1 km of a point
const comps = await call("POST", "/v1/comparables/search", {
  comparables_count: 5,
  operation: "sale",
  comparables_types: ["apartment"],
  bedrooms: 2,
  location_boundary: {
    circle: { distance: 1, target_point: { coordinates: { latitude: 40.4168, longitude: -3.7038 } } },
  },
});
console.log(JSON.stringify(comps, null, 2).slice(0, 800));

// 3. Claro: commercial premises in Spain from a brief in plain words
const claro = await call("POST", "/v1/claro/search?limit=5", {
  brief: "Burger restaurant in Madrid, ground floor, 120-250 m2, smoke outlet, rent under 8,000 a month",
});
console.log(JSON.stringify(claro, null, 2).slice(0, 800));
