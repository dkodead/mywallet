"""Categorisation of articles into high‑level topics.

This module assigns categories (e.g. 'Greece', 'Netherlands', 'Data Science',
'AI', 'Finance') to articles based on simple keyword matching.  If an article
already has a category assigned, it will not be modified.  The classifier is
rudimentary but sufficient for demonstration purposes; in production you may
wish to use a more sophisticated model or ruleset.
"""

from __future__ import annotations

from typing import Iterable
import re

from .datatypes import Article


CATEGORY_KEYWORDS = {
    'Greece': [r'\bGreece\b', r'Greek', r'Athens', r'Crete'],
    'Netherlands': [r'\bNetherlands\b', r'Dutch', r'Amsterdam', r'Rotterdam'],
    'Data Science': [r'data science', r'dataset', r'data scientist', r'machine learning'],
    'AI': [r'AI', r'artificial intelligence', r'GPT', r'LLM', r'neural network'],
    'Finance': [r'bank', r'finance', r'stock', r'economy', r'interest rate', r'bitcoin', r'NASDAQ', r'ECB'],
}


def classify_articles(articles: Iterable[Article]) -> None:
    """Assign categories to articles lacking them based on keywords.

    This function modifies the articles in place.  Articles with an existing
    category are left unchanged.
    """
    for article in articles:
        if article.category:
            continue
        text = f"{article.title} {article.description}".lower()
        assigned = False
        for cat, patterns in CATEGORY_KEYWORDS.items():
            for pattern in patterns:
                if re.search(pattern.lower(), text):
                    article.category = cat
                    assigned = True
                    break
            if assigned:
                break
        if not article.category:
            article.category = 'Unknown'
