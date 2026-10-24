# Comparables by Casafari: review information

Not packaged in the zip; paste into the submission form. Reviewer sign-in is the same as Claro's (`docs/handoff-openai-databricks-2026-10-20.md` in casafari/premises): `mcp-review@theaicompany.org`, organisation Casafari-MCP, one-time email code.

Server: `https://platform.casafari.com/mcp/comparables` (OAuth).

## Test cases

| # | Scenario | User prompt | Tool | Expected output |
|---|---|---|---|---|
| 1 | Value a flat from an address | What is a 90 m² two-bedroom flat at Calle de Alcalá 120, Madrid worth on the sale market? | `comparables_get_comparables` | An estimated sale price with its range and price per m², the comparable properties behind it (size, price, distance), the radius and filters used, Casafari as source. |
| 2 | Rental comparables for a shop | Find rental comparables for a 150 m² street-level shop in Lisbon's Baixa, within 500 m. | `comparables_get_comparables` | Comparable retail properties for rent within 0.5 km with area, rent, rent per m² and distance, plus an estimated rent range. |
| 3 | Registry sales in Spain | Show official registry sale prices for flats sold since January 2025 within 1 km of Plaça de Catalunya, Barcelona. | `comparables_get_comparables` | Registry sale records (date, price, area, price per m²) since 2025-01-01 within 1 km, with the source named. |
| 4 | Rent estimate outside Spain | Estimate the monthly rent of a 70 m² two-bedroom apartment near Rue Royale in Brussels. | `comparables_get_comparables` | An estimated monthly rent with its range and the rental comparables behind it. |
| 5 | Account status | How many Casafari tokens does my organisation have left? | `account_status` | The organisation's remaining tokens and plan; free, nothing charged. |

## Negative test cases

| # | Scenario | User prompt |
|---|---|---|
| 1 | Asks for a property portal link; Comparables never names or links portals. | Give me the portal links where these comparable flats are advertised so I can contact the owners. |
| 2 | A country outside coverage. | Value a 3-bedroom house in Austin, Texas. |
| 3 | A legal or tax question; Comparables has no legal tools. | How much capital gains tax will I pay in Spain if I sell my flat for €400,000? |

## Release notes

```
First release of Comparables by Casafari in ChatGPT.

- Value any property from an address, a point or, in Spain, a cadastral reference: estimated sale price or rent with its range.
- See the comparable properties behind every estimate: size, price, price per m² and distance.
- In Spain, official registry sale prices.
- Homes and commercial property in Andorra, Austria, Belgium, France, Germany, Greece, Italy, Luxembourg, Monaco, Poland, Portugal, San Marino, Spain and Switzerland.
- Sign in with your Casafari API and MCP Platform account; Comparables only reads data.
```
