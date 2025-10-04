"""Data classes used by the news engine.

The `Article` data class represents a single news article after normalisation.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """Represents a normalised news article.

    Attributes
    ----------
    title: str
        The headline of the article.
    link: str
        The canonical URL to the article.
    description: str
        A short description or excerpt from the article.
    published: datetime
        Publication timestamp (naive UTC).
    publisher: str
        Name of the outlet that published the article.
    category: Optional[str]
        The high‑level category assigned to the article (e.g. 'Greece').
    """

    title: str
    link: str
    description: str
    published: datetime
    publisher: str
    category: Optional[str] = None
