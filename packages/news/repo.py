"""Simple SQLite repository for storing and retrieving news topics.

This module provides functions to persist the output of the news pipeline and
retrieve top topics for a given category.  Each topic is stored as a single
row in a `clusters` table.  Articles themselves are not stored; the topic
record contains the headline, summary, importance, publication time, list of
sources and list of links as plain text.

The database schema is created automatically if it does not exist.
"""

from __future__ import annotations

import sqlite3
from typing import Dict, List
import os
import json


def init_db(db_path: str) -> None:
    """Initialise the SQLite database and create tables if necessary."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS clusters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                headline TEXT NOT NULL,
                summary TEXT NOT NULL,
                importance REAL NOT NULL,
                published TEXT NOT NULL,
                sources TEXT NOT NULL,
                links TEXT NOT NULL
            );
            """
        )
        # Optional index to speed up queries by category and importance
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_clusters_category_importance
            ON clusters (category, importance DESC);
            """
        )
        conn.commit()


def save_pipeline_output(results: Dict[str, List[Dict]], db_path: str) -> None:
    """Persist the results of a pipeline run into the database.

    Parameters
    ----------
    results: dict
        The dictionary returned by :func:`run_pipeline`.  Keys are category
        names and values are lists of topic dictionaries.
    db_path: str
        Path to the SQLite database file.
    """
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        for category, topics in results.items():
            for topic in topics:
                cur.execute(
                    """
                    INSERT INTO clusters (category, headline, summary, importance, published, sources, links)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        category,
                        topic['headline'],
                        topic['summary'],
                        float(topic['importance']),
                        topic['published'],
                        json.dumps(topic['sources']),
                        json.dumps(topic['links']),
                    ),
                )
        conn.commit()


def fetch_top_topics(category: str, db_path: str, limit: int = 4) -> List[Dict]:
    """Retrieve the most important topics for a given category.

    Parameters
    ----------
    category: str
        The category for which to fetch topics.
    db_path: str
        Path to the SQLite database file.
    limit: int, default 4
        Maximum number of topics to return.

    Returns
    -------
    list of dict
        A list of topic dictionaries in the same format as produced by
        :func:`run_pipeline`.  If the database file does not exist or the
        category has no stored topics, an empty list is returned.
    """
    if not os.path.exists(db_path):
        return []
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT headline, summary, importance, published, sources, links
            FROM clusters
            WHERE category = ?
            ORDER BY importance DESC, datetime(published) DESC
            LIMIT ?;
            """,
            (category, limit),
        )
        rows = cur.fetchall()
    topics: List[Dict] = []
    for headline, summary, importance, published, sources_json, links_json in rows:
        try:
            sources = json.loads(sources_json)
        except Exception:
            sources = []
        try:
            links = json.loads(links_json)
        except Exception:
            links = []
        topics.append({
            'headline': headline,
            'summary': summary,
            'importance': importance,
            'published': published,
            'sources': sources,
            'links': links,
        })
    return topics


def fetch_daily_digest(db_path: str, categories: List[str], limit: int = 4) -> Dict[str, List[Dict]]:
    """Return a dictionary of top topics for multiple categories.

    This convenience function wraps :func:`fetch_top_topics` for multiple
    categories.
    """
    digest: Dict[str, List[Dict]] = {}
    for category in categories:
        digest[category] = fetch_top_topics(category, db_path, limit)
    return digest
