"""Clustering of articles into topics.

This module uses TF‑IDF vectorisation and DBSCAN to group similar articles into
topics.  Articles in the same cluster are assumed to describe the same event or
story.  The clustering is unsupervised and based solely on the textual
similarity of article titles and descriptions.
"""

from __future__ import annotations

from typing import List, Iterable
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances
import numpy as np

from .datatypes import Article


def cluster_articles(articles: Iterable[Article], eps: float = 0.5, min_samples: int = 1) -> List[List[Article]]:
    """Group similar articles into clusters using TF‑IDF and DBSCAN.

    Parameters
    ----------
    articles: iterable of Article
        A list of articles to cluster.
    eps: float, default 0.5
        The maximum cosine distance between two samples for them to be considered in the same neighbourhood.  A smaller value yields more clusters.
    min_samples: int, default 1
        The number of samples in a neighbourhood for a point to be considered as a core point.

    Returns
    -------
    list of list of Article
        A list of clusters, each containing the articles that were grouped together.
    """
    articles = list(articles)
    if not articles:
        return []

    # Build corpus from title + description
    corpus = [f"{a.title} {a.description}" for a in articles]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(corpus)
    # Compute cosine distances (1 - similarity)
    distance_matrix = cosine_distances(X)
    # DBSCAN expects distances; metric='precomputed' uses the distance matrix directly
    db = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed')
    labels = db.fit_predict(distance_matrix)

    clusters: dict[int, List[Article]] = {}
    for label, article in zip(labels, articles):
        clusters.setdefault(label, []).append(article)
    # Convert to list and sort clusters by recency (most recent first)
    cluster_list = list(clusters.values())
    cluster_list.sort(key=lambda cl: max(a.published for a in cl), reverse=True)
    return cluster_list
