"""FastAPI application exposing news and banking endpoints."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from typing import Dict, List
from datetime import datetime, timedelta

import os
from ...packages.news.pipeline import run_pipeline
from ...packages.news import repo as news_repo
from ...packages.banks.providers import DemoBankProvider

app = FastAPI(title="wallet.dkoded.io API")

# Determine the path to the SQLite database for storing news topics.  You can
# override this via the DATABASE_PATH environment variable.  By default it
# resides under wallet_dkoded/data/news.db.
_default_db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
os.makedirs(_default_db_dir, exist_ok=True)
DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join(_default_db_dir, 'news.db'))

# Define the categories known to the system.  If you add new categories to the
# pipeline, include them here so that the API knows which to return.
CATEGORIES = ["Greece", "Netherlands", "Data Science", "AI", "Finance"]


@app.get("/news/daily")
async def get_daily_news() -> Dict[str, List[Dict]]:
    """Return the top topics for each category from the last 24 hours.

    This endpoint first tries to fetch topics from the database.  If there are
    no topics stored (e.g. on first run), it executes the pipeline and
    persists the output before returning the fresh results.
    """
    # Attempt to read from DB
    digest = news_repo.fetch_daily_digest(DATABASE_PATH, CATEGORIES)
    if all(digest.get(cat) for cat in CATEGORIES):
        return digest
    # If no data yet, run the pipeline and store results
    results = run_pipeline(use_sample=True, store_to_db=True, db_path=DATABASE_PATH)
    return results


@app.get("/news/breaking")
async def get_breaking_news() -> List[Dict]:
    """Return breaking news topics with high importance in the last hour."""
    # Fetch the most recent topics from the DB for all categories
    import json
    from datetime import datetime, timedelta

    now = datetime.utcnow()
    breaking: List[Dict] = []
    for category in CATEGORIES:
        topics = news_repo.fetch_top_topics(category, DATABASE_PATH, limit=10)
        for topic in topics:
            try:
                published = datetime.fromisoformat(topic['published'])
            except Exception:
                continue
            if (now - published) <= timedelta(hours=1) and topic['importance'] >= 0.7:
                topic_with_cat = topic.copy()
                topic_with_cat['category'] = category
                breaking.append(topic_with_cat)
    return breaking


@app.get("/banks/balances")
async def get_bank_balances() -> List[Dict]:
    """Return the user's account balances from the demo provider."""
    provider = DemoBankProvider()
    return provider.get_balances()


@app.post("/news/update")
async def update_news() -> Dict:
    """Trigger the news pipeline manually and persist the results.

    This endpoint runs the pipeline with sample data (or live RSS if configured),
    stores the output to the SQLite database, and returns a simple status
    message indicating success along with the list of updated categories.
    """
    results = run_pipeline(use_sample=True, store_to_db=True, db_path=DATABASE_PATH)
    return {"status": "updated", "categories": list(results.keys())}
