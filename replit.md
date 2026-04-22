# CogniScan — Cognitive Insight Hub (Python)

## Overview

A pure-Python rebuild of the CogniScan cognitive insight platform from the
`Sanjeevini210704/Cognitive-Insight-Hub` GitHub repo. It analyzes social-media
consumption patterns and surfaces cognitive/emotional signals through five
interactive charts.

## Stack

- **Language**: Python 3.11 (only)
- **UI / Web framework**: Streamlit
- **Database**: Local MongoDB-compatible store via `montydb` (PyMongo-style API,
  persists to local SQLite files under `cogni_scan/data/`)
- **Charts**: Plotly
- **Auth**: bcrypt password hashing

## Run

```
streamlit run app.py --server.port 5000
```

The "Start application" workflow is preconfigured.

## Project Layout

```
app.py                # Streamlit entry point (router + pages)
cogni_scan/
  db.py               # MontyDB local MongoDB connection (users, analyses)
  auth.py             # bcrypt login/register, seed users
  analyzer.py         # Rule-based cognitive analysis engine
  charts.py           # 5 Plotly charts
  data/               # Local DB files (gitignored)
.streamlit/config.toml
```

## Demo Credentials

- User:  `demo@cogniscan.ai` / `demo1234`
- Admin: `admin@cogniscan.ai` / `admin1234`

## Pages

- Landing (`/`)
- User Login + Register
- Admin Login
- User Dashboard — paste content, run analysis, view 5 charts, Print / New
  Analysis / Logout
- History — past analyses for the logged-in user
- Admin Dashboard — totals, users table, all analyses, platform stats

## Five Analysis Charts

1. Radar — Cognitive Metrics (attention, anxiety, dopamine, social comparison,
   info overload)
2. Donut — Content category breakdown
3. Stacked Bar — Emotional trend (positive / negative / neutral by day)
4. Area — Engagement pattern by hour
5. Horizontal Bar — Risk factor severity

## Notes

The `artifacts/` and `lib/` directories from the original Replit pnpm template
are unused by this Python build and can be ignored.
