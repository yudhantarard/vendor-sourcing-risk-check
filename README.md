# SHIFT Vendor Sourcing & Risk Check

Search for suppliers, shortlist the candidates, then run a preliminary due-diligence screen.
Built for procurement teams. A screening aid, **not** compliance clearance.

## Flow
1. **Search** a company name ("PT Astra International") or a category ("percetakan packaging Bekasi").
2. **Shortlist** from map results (free OpenStreetMap by default, Google Places if a key is set): name, address, website, sector, and rating where available. Filter by rating and operational status. Vendors without a Maps listing can be added manually.
3. **Risk check** the ticked vendors: Google News headlines are screened against a transparent keyword list, giving a LOW / MEDIUM / HIGH Preliminary Risk Indicator, findings and a recommended procurement action, side by side in one comparison table.

## Architecture
```
app.py                 UI and flow
services/search.py     Dispatcher: Google if key set, else OpenStreetMap, else labelled mock
services/osm.py        OpenStreetMap: Nominatim (names) + Overpass (categories in a city)
services/places.py     Google Places API (New) Text Search (optional)
services/sector.py     Sector from map type/tag (no AI)
services/news.py       Google News RSS
services/risk.py       Keyword risk engine (swappable)
services/screening.py  Runs risk for one or many vendors
data/                  sector list, Maps-type mapping, risk keywords, mock vendors
utils/                 helpers, SHIFT styling
```

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```
No key needed: search runs on OpenStreetMap. Optionally copy
`.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` for `APP_PASSWORD` and an optional `GOOGLE_PLACES_API_KEY` (paid). Never commit the real secrets file.
Deployment steps: see `GITHUB_GUIDE.md`.

## Methodology and limits
- Sector comes from the map type/tag through `data/sectors.py`. Generic or missing types give "Other / unclear", editable per vendor.
- Risk level: any HIGH keyword in a headline gives HIGH, else any MEDIUM keyword gives MEDIUM, else LOW. Keywords are in `data/risk_keywords.py`.
- Headlines only, context-blind: expect false positives and negatives. Similar company names can return unrelated news.
- Only businesses present in the map data appear. OpenStreetMap coverage of Indonesian B2B firms is thin and has no ratings; category search covers only the words in `CATEGORY_TAGS`. Nominatim/Overpass fair-use limits apply. No registry, sanctions, PEP, litigation or financial data yet.
- Absence of adverse media does not indicate absence of risk. A person makes the decision.

## Roadmap
Entity matching · sanctions/PEP lists · corporate registry (AHU/OSS) · litigation and financial data · CSV import/export · multi-dimension risk score · audit log.
