# Energy Flexibility Pipeline

A backend system that ingests real German electricity price and weather data to 
decide the cheapest, most solar-friendly hours to run a home heat pump or charge 
a battery.

**Status: work in progress.** See roadmap below for what's done vs. planned.

## What it does

- Ingests real day-ahead electricity prices for Germany (SMARD.de)
- Ingests real hourly solar radiation data (DWD's DUETT dataset)
- (Planned) Runs a rule-based, explainable optimizer that schedules a synthetic 
  household's heat pump/battery usage to minimize cost and maximize solar self-use
- (Planned) Serves everything via a FastAPI backend, backed by Postgres

## Data sources & decisions

- **Prices:** SMARD.de day-ahead auction prices, chosen over ENTSO-E for no-auth simplicity. 
- **Weather:** DWD's DUETT dataset (hourly global solar radiation, combined satellite + ground-station product). Only the `FG_DUETT` radiation value is used. The quality-level flag (`QN_952`) and uncertainty column (`FG_UN_DUETT`) are intentionally not used — this project scopes to point-in-time radiation values, not formal quality filtering. 
- **Historical backfill:** ~2-4 weeks of both prices and weather, ingested to support backtesting (not needed for the optimizer's day-to-day logic, which only ever looks at one day at a time).


## Tech stack

Python, Postgres, FastAPI (planned), Docker, pytest, GitHub Actions CI (planned)

## Roadmap

- [x] Repo scaffolding, environment setup
- [x] Price ingestion (SMARD): fetch + parse
- [x] Weather ingestion (DWD DUETT): fetch + parse
- [x] Postgres schema + docker-compose setup
- [x] Persist ingested data to Postgres
- [ ] Synthetic household load + PV profile generator
- [ ] Rule-based optimizer
- [ ] FastAPI backend + tests
- [ ] Dockerize + CI
- [ ] (Stretch) Dashboard, live deploy

## Running locally

Instructions coming as ingestion and the API are completed.

## Caveats
- DUETT radiation values are "pseudo-station" — interpolated from a 5km satellite+ground blended grid, not raw sensor readings everywhere.
- Prices are fixed, published day-ahead values, not forecasts.

## Future improvements

- [ ] Scrape DWD's Stationen.txt to resolve station names to IDs automatically
