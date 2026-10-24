# Area Insights by Casafari: review information

Not packaged in the zip; paste into the submission form. Reviewer sign-in is the same as Claro's (`docs/handoff-openai-databricks-2026-10-20.md` in casafari/premises): `mcp-review@theaicompany.org`, organisation Casafari-MCP, one-time email code.

Server: `https://platform.casafari.com/mcp/area-insights` (OAuth).

## Test cases

| # | Scenario | User prompt | Tool | Expected output |
|---|---|---|---|---|
| 1 | Price trend | How has the average asking price per m² of flats for sale in Lisbon changed each quarter over the last three years? | `locations_search`, `area-insights_get_time_series_data` | Quarterly price per m² for Lisbon over three years, with period, filters and Casafari as source. |
| 2 | Growth figure | What is the compound annual growth rate of flat prices per m² in Valencia since 2021? | `area-insights_get_time_series_operations` | A CAGR figure with the series it was computed from and the period. |
| 3 | District comparison | Which districts of Madrid have the highest asking rents per m² for flats? | `area-insights_get_heatmap` | Madrid's districts ranked by rent per m², with the period and filters. |
| 4 | Price spread | How are asking prices of houses for sale spread in Munich: how many in each price band? | `area-insights_get_price_distribution` | Counts of properties per price band for Munich, with filters. |
| 5 | Time on market | How long do apartments for sale stay on the market in Nice? | `area-insights_get_time_on_market_distribution` | Counts of properties per time-on-market band, with the median where given. |

## Negative test cases

| # | Scenario | User prompt |
|---|---|---|
| 1 | Asks to list and link individual properties from portals; Area Insights gives aggregated statistics only. | List the 20 cheapest flats for sale in Porto with links to the portals that advertise them. |
| 2 | A country outside coverage. | What are average rents in Dubai Marina? |
| 3 | Investment advice; Area Insights reports data, not recommendations. | Should I buy a flat in Barcelona now or wait until prices fall next year? |

## Release notes

```
First release of Area Insights by Casafari in ChatGPT.

- Price and rent trends per week, month, quarter or year for any area, with growth and volatility figures.
- Price, bedroom and time-on-market distributions, and heatmaps comparing a city's districts.
- Place names resolve to locations for free on the same connector.
- Coverage: Andorra, Austria, Belgium, France, Germany, Greece, Italy, Luxembourg, Monaco, Poland, Portugal, San Marino, Spain and Switzerland.
- Sign in with your Casafari API and MCP Platform account; Area Insights only reads data.
```
