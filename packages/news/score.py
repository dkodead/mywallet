"""Importance scoring for news clusters.

This module assigns an importance score to each cluster of articles.  The score
is a weighted combination of cross‑source coverage (number of unique
publishers) and recency.  Both components are normalised across all clusters
such that the resulting score lies in the interval [0, 1].  Additional
components (e.g. social engagement) could be added in a real deployment.
"""

from __future__ import annotations

from typing import List, Tuple
from datetime import datetime

from .datatypes import Article


def _compute_source_coverage(cluster: List[Article]) -> int:
    return len(set(article.publisher for article in cluster))


def _compute_recency(cluster: List[Article], now: datetime) -> float:
    """Compute the age of the most recent article in hours."""
    latest = max(article.published for article in cluster)
    delta = now - latest
    return delta.total_seconds() / 3600.0  # hours


def score_clusters(clusters: List[List[Article]]) -> List[Tuple[List[Article], float]]:
    """Score each cluster based on source coverage and recency.

    Returns a list of pairs `(cluster, score)` sorted by score descending.
    """
    now = datetime.utcnow()
    if not clusters:
        return []

    coverages = [float(_compute_source_coverage(c)) for c in clusters]
    # Recency in hours (lower is better) so invert later
    ages = [_compute_recency(c, now) for c in clusters]

    max_cov = max(coverages) or 1.0
    max_age = max(ages) or 1.0

    # Normalise coverage and recency.  More sources => higher score.  More recent => higher score.
    norm_cov = [c / max_cov for c in coverages]
    norm_recency = [1.0 - (age / max_age) for age in ages]  # invert: 0 oldest, 1 most recent

    scores: List[float] = []
    for cov, rec in zip(norm_cov, norm_recency):
        # Weighted combination (70% cross‑source, 30% recency)
        scores.append(0.7 * cov + 0.3 * rec)

    scored = list(zip(clusters, scores))
    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
