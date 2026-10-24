# Location Lookup by Casafari: review information

Not packaged in the zip; paste into the submission form. Reviewer sign-in is the same as Claro's (`docs/handoff-openai-databricks-2026-10-20.md` in casafari/premises): `mcp-review@theaicompany.org`, organisation Casafari-MCP, one-time email code.

Server: `https://platform.casafari.com/mcp/locations` (OAuth).

## Test cases

| # | Scenario | User prompt | Tool | Expected output |
|---|---|---|---|---|
| 1 | Find a neighbourhood | Find the Casafari location id for the Chamberí district of Madrid. | `locations_search` | Chamberí with its location id, kind (district) and parents (Madrid, Madrid Province, Community of Madrid, Spain). |
| 2 | Ambiguous name | Which places called Santa Cruz does Casafari know in Spain and Portugal? | `locations_search` | Several matches, each with id, type, country and parents, shown for the person to choose; no guess. |
| 3 | Details of an id | Give me the details of the location you found for Chamberí. | `locations_get` | The location's id, name, type and its parent hierarchy. |
| 4 | Another country | Find the location id for Schwabing in Munich. | `locations_search` | Schwabing with its id, kind (district) and parents (Munich, Bayern, Germany). |
| 5 | City in France | What is Casafari's location id for Lyon, France? | `locations_search` | Lyon with its id, kind (city) and parents (Rhône, Rhône-Alpes, France). |

## Negative test cases

| # | Scenario | User prompt |
|---|---|---|
| 1 | Asks for property prices; Location Lookup only resolves places. | What is the average price per m² in Chamberí? |
| 2 | A place outside coverage. | Find the location id for Brooklyn, New York. |
| 3 | Directions; Location Lookup has no routing. | How do I drive from Madrid to Valencia avoiding tolls? |

## Release notes

```
First release of Location Lookup by Casafari in ChatGPT.

- Find any place by name, from a country to a neighbourhood, with its Casafari location id, type and parents.
- Free to call; use the ids with Comparables and Area Insights by Casafari.
- Coverage: Andorra, Austria, Belgium, France, Germany, Greece, Italy, Luxembourg, Monaco, Poland, Portugal, San Marino, Spain and Switzerland.
- Sign in with your Casafari API and MCP Platform account.
```
