"""Article ingestion for the news engine.

The ingestion layer fetches articles from RSS feeds or loads sample data when
network access is unavailable.  Each article is converted into a normalised
:class:`~packages.news.datatypes.Article` instance.
"""

from __future__ import annotations

from typing import List, Dict, Iterable
from datetime import datetime
import logging
import xml.etree.ElementTree as ET

import requests

from .datatypes import Article
from .sample_data import load_sample_articles


logger = logging.getLogger(__name__)

# Mapping from category to a list of RSS feed URLs.  These feeds are not used
# in this offline environment, but they illustrate how to configure the
# ingestion layer when network access is available.  Replace or extend these
# URLs when deploying in production.
RSS_SOURCES: Dict[str, List[str]] = {
    "Greece": [
        # Example: "https://www.kathimerini.gr/rss"
    ],
    "Netherlands": [
        # Example: "https://nos.nl/rss"
    ],
    "Data Science": [
        # Example: "https://www.oreilly.com/radar/feed/"
    ],
    "AI": [
        # Example: "https://openai.com/blog/rss/"
    ],
    "Finance": [
        # Example: "https://www.reuters.com/rssFeed/businessNews"
    ],
}


def _parse_rss(content: bytes, category: str) -> List[Article]:
    """Parse an RSS feed and return a list of articles.

    Parameters
    ----------
    content: bytes
        Raw XML content of the RSS feed.
    category: str
        Category name to assign to each article.
    """
    articles: List[Article] = []
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        logger.warning("Failed to parse RSS feed: %s", exc)
        return articles

    # RSS items may be nested under channel/item or rss/channel/item
    for item in root.iter('item'):
        title = item.findtext('title') or ''
        link = item.findtext('link') or ''
        description = item.findtext('description') or ''
        pub_date_str = item.findtext('pubDate') or ''
        published: datetime
        if pub_date_str:
            try:
                published = datetime.strptime(pub_date_str[:25], "%a, %d %b %Y %H:%M:%S")
            except Exception:
                published = datetime.utcnow()
        else:
            published = datetime.utcnow()
        # Extract domain as publisher
        publisher = ''
        try:
            from urllib.parse import urlparse
            netloc = urlparse(link).netloc
            publisher = netloc.split(':')[0]
        except Exception:
            publisher = ''
        articles.append(Article(title=title.strip(), link=link.strip(), description=description.strip(), published=published, publisher=publisher, category=category))

    return articles


def fetch_articles_from_feeds() -> List[Article]:
    """Fetch articles from the configured RSS feeds.

    When network access is disabled, this function will return an empty list.
    If network access is available, it attempts to download each configured feed
    and parse it into a list of :class:`Article` objects.
    """
    all_articles: List[Article] = []
    for category, feeds in RSS_SOURCES.items():
        for url in feeds:
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
            except Exception as exc:
                logger.info("Skipping RSS feed %s: %s", url, exc)
                continue
            articles = _parse_rss(resp.content, category)
            all_articles.extend(articles)
    return all_articles


def load_articles(use_sample: bool = True) -> List[Article]:
    """Load articles either from RSS feeds or from sample data.

    Parameters
    ----------
    use_sample: bool, default True
        If True, returns the built‑in sample articles.  If False and at least
        one RSS feed is configured, attempts to fetch real articles.  When
        network access is unavailable, this will simply return an empty list.
    """
    if use_sample:
        return load_sample_articles()
    # Attempt to fetch real articles
    articles = fetch_articles_from_feeds()
    if not articles:
        logger.warning("No articles fetched from RSS feeds; falling back to sample data.")
        return load_sample_articles()
    return articles
