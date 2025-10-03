# wallet.dkoded.io

This repository contains a prototype implementation for **wallet.dkoded.io**, a personal dashboard that fuses banking information with an intelligent news engine.  The project is organised as a monorepo with separate applications and shared packages.  Although the environment used to build this example does not allow outgoing network connections or the installation of additional dependencies, the code is structured to support real integrations when run in a proper environment.

## Overview

The goal of this project is to provide a unified dashboard where a user can:

* **View recent transactions and account balances** via a provider‑agnostic banking adapter.  The current implementation includes stubs for Plaid, TrueLayer and Tink.
* **Follow relevant news** across the topics *Greece*, *Netherlands*, *Data Science*, *AI* and *Finance*.  The news engine fetches articles (via RSS, if configured), clusters them to remove duplicates, scores them for importance and summarises the top stories for each category.
* **Log in with Google** on the front‑end.  A Next.js skeleton is provided in `apps/web` along with instructions for enabling Google sign‑in using NextAuth.

## Repository structure

```
wallet_dkoded/
│
├── apps/
│   ├── api/        # FastAPI application exposing news and banking endpoints
│   └── web/        # Next.js frontend (skeleton) with dark navy theme
│
├── packages/
│   ├── banks/      # Provider‑agnostic banking adapter interfaces and stubs
│   ├── news/       # News ingestion, clustering, scoring and summarisation
│   └── ui/         # Shared React components (skeleton)
│
├── infra/          # Infrastructure templates (e.g. Dockerfile, docker‑compose)
└── scripts/
    └── run_pipeline.py  # Example script to run the news pipeline on sample data
```

### apps/api

The `apps/api` directory defines a **FastAPI** server that exposes a REST API:

* `GET /news/daily` — returns the stored top four topics for each category.  If the news database is empty, it runs the news pipeline, persists the results to a SQLite database (`data/news.db`) and returns the fresh output.
* `GET /news/breaking` — returns high‑importance topics published within the last hour from the database.
* `POST /news/update` — triggers the news pipeline manually, storing the latest results to the database and returning a status object.  Use this endpoint to refresh the news on demand.
* `GET /banks/balances` — placeholder endpoint returning dummy bank balances.

These endpoints rely on the functions defined in the `packages/news` and `packages/banks` packages.  The news data is persisted in a local SQLite database by default; you can override the path via the `DATABASE_PATH` environment variable.  To start the API locally, run:

```sh
python -m uvicorn apps.api.main:app --reload
```

### apps/web

The `apps/web` directory contains a **Next.js** skeleton using TypeScript and Tailwind CSS.  It includes a basic page layout with navigation links and placeholders for the news and wallet sections.  The project is set up to use `shadcn/ui` for UI components and `tremor` for charts.  To enable Google sign‑in you should install `next-auth` and configure a Google provider with your OAuth credentials.  See the comments in `apps/web/pages/_app.tsx` for guidance.

> **Note:** This environment cannot install additional npm packages or fetch external assets.  The web app provided here is a scaffold only; you will need to run `npm install` in an Internet‑enabled environment to install Next.js, NextAuth, shadcn/ui and Tremor.

### packages/news

This package implements the news pipeline.  It defines data classes and functions for:

* **Ingesting** articles from RSS feeds (via the standard library) or sample data when network access is unavailable.
* **Clustering** articles using TF‑IDF vectors and DBSCAN to group near‑duplicate items.
* **Scoring** clusters based on the number of distinct publishers, recency and basic engagement heuristics.
* **Summarising** clusters with a simple frequency‑based summariser built on NLTK.
* **Running** the pipeline end‑to‑end and returning the top four topics per category.
* **Persisting** pipeline results to a local SQLite database (`data/news.db`) when requested.  The repository functions in `packages/news/repo.py` handle saving and retrieving clusters.  The API layer uses these functions to serve stored content by default.

The pipeline is deterministic and works entirely offline with sample data defined in `packages/news/sample_data.py`.  When you deploy to a real environment with network access, you can modify the `RSS_SOURCES` dictionary in `packages/news/ingest.py` to fetch from real RSS feeds.

### Database persistence

The news pipeline can persist its results to a SQLite database.  The database file is located under `wallet_dkoded/data/news.db` by default (controlled via the `DATABASE_PATH` environment variable).  The `apps/api` service reads from this database whenever possible, falling back to running the pipeline when it is empty.  To trigger a refresh manually, send a `POST` request to `/news/update`.

### packages/banks

This package defines a small interface for interacting with banking APIs.  It includes an abstract `BankProvider` class and stub implementations for `PlaidProvider`, `TrueLayerProvider` and `TinkProvider`.  These stubs return dummy data.  When you integrate with a real provider, implement the required methods in the appropriate provider class.

### packages/ui

Contains shared React components.  For now, there is a placeholder `NavBar` component.  You can extend this with additional components and design tokens as the front‑end develops.

### scripts/run_pipeline.py

This script demonstrates how to run the news pipeline on the sample data and output the results as JSON.  Running this script in the current environment will produce the top four topics for each category and print them to the console.

## Getting started

1. **Clone this repository** and navigate into the `wallet_dkoded` directory.
2. **Set up a Python virtual environment** and install dependencies.  A `requirements.txt` file is included.
3. **Run the news pipeline** using `python scripts/run_pipeline.py` to see sample results.
4. **Start the API** with Uvicorn (`python -m uvicorn apps.api.main:app --reload`) to expose the endpoints locally.
5. **Navigate into `apps/web`** and run `npm install` in an Internet‑enabled environment to install Next.js and its dependencies.  Then start the dev server with `npm run dev` to view the front‑end.

## Future work

* Replace the sample news ingestion logic with real RSS/API calls once network access is available.
* Implement proper clustering (e.g. using sentence embeddings with `sentence-transformers` and HDBSCAN) for improved topic grouping.
* Enhance the importance scoring by incorporating social signals and front‑page prominence.
* Build out the front‑end to include charts, tables and interactive filters for both news and financial data.
* Flesh out the banking adapters to communicate with Plaid, TrueLayer or Tink in production.
* Add authentication flows (Google sign‑in) using NextAuth on the web app.
