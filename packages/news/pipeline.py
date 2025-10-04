"""End‑to‑end news pipeline.

This module orchestrates the ingestion, classification, clustering, scoring and
summarisation of news articles.  It exposes a single function
:func:`run_pipeline` which returns a dictionary containing the top topics per
category.  Each topic includes the best headline, a summary, a list of
sources, importance score and publication time.
"""

from __future__ import annotations

from typing import Dict, List, Iterable
from datetime import datetime, timedelta

from .ingest import load_articles
from .classify import classify_articles
from .cluster import cluster_articles
from .score import score_clusters
from .summarize import summarize_cluster
from .datatypes import Article


def run_pipeline(use_sample: bool = True, *, store_to_db: bool = False, db_path: str = None) -> Dict[str, List[Dict]]:
    """Run the news pipeline and return top topics per category.

    Parameters
    ----------
    use_sample: bool, default True
        If True, loads articles from the built‑in sample data.  If False,
        attempts to fetch from RSS feeds.  When network access is unavailable,
        this argument is ignored and sample data is used.

    Returns
    -------
    dict
        A dictionary keyed by category name.  Each value is a list of up to
        four topic dictionaries, sorted by importance descending.  Each topic
        contains the following fields:

        ``headline``: The best headline for the topic (taken from the most recent article).
        ``summary``: A short summary of the topic.
        ``importance``: Importance score between 0 and 1.
        ``published``: ISO 8601 timestamp of the most recent article in the cluster.
        ``sources``: List of unique publishers covering the topic.
        ``links``: List of URLs to the articles in the cluster.
    """
    # Ingest articles
    articles: List[Article] = load_articles(use_sample=use_sample)
    # Assign categories if missing
    classify_articles(articles)
    # Group by category
    articles_by_category: Dict[str, List[Article]] = {}
    for article in articles:
        articles_by_category.setdefault(article.category, []).append(article)

    results: Dict[str, List[Dict]] = {}

    for category, articles_in_cat in articles_by_category.items():
        # Cluster articles within this category
        clusters = cluster_articles(articles_in_cat)
        # Score clusters
        scored = score_clusters(clusters)
        # Build topic summaries
        topics: List[Dict] = []
        for cluster, score in scored:
            if not cluster:
                continue
            # Determine best article (most recent) for the headline
            best_article = max(cluster, key=lambda a: a.published)
            summary = summarize_cluster(cluster)
            topics.append({
                'headline': best_article.title,
                'summary': summary,
                'importance': round(score, 3),
                'published': best_article.published.isoformat(),
                'sources': list({a.publisher for a in cluster}),
                'links': [a.link for a in cluster],
            })
        # Keep top 4 topics
        results[category] = topics[:4]

    # If configured, persist the results to a SQLite database
    if store_to_db:
        try:
            from . import repo as news_repo  # local import to avoid circular
            # Derive a default DB path if not supplied
            if db_path is None:
                # Create a data directory relative to this file
                import os
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                data_dir = os.path.join(base_dir, 'data')
                os.makedirs(data_dir, exist_ok=True)
                db_path = os.path.join(data_dir, 'news.db')
            news_repo.save_pipeline_output(results, db_path)
        except Exception as exc:
            # Log the error but do not interrupt the pipeline
            import logging
            logging.getLogger(__name__).warning("Failed to persist pipeline output: %s", exc)

    return results
