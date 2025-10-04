"""Summarisation utilities for news clusters.

This module provides a simple extractive summariser that selects the most
important sentences from a piece of text.  It uses NLTK to tokenise sentences
and words and ranks sentences by the sum of word frequencies (excluding
punctuation and common stopwords).  The summariser is deliberately minimal so
that it works without external models; when running in a richer environment
you may replace it with a more sophisticated summarisation method.
"""

from __future__ import annotations

from typing import List
import re
# Attempt to import NLTK tokenizers and stopwords.  If NLTK data is not
# available (as may be the case in offline environments), we fall back to
# simple regex-based tokenisation and a small list of stopwords.
try:
    from nltk import sent_tokenize, word_tokenize  # type: ignore
    from nltk.corpus import stopwords  # type: ignore
    # Try to access the stopwords corpus.  This may raise a LookupError if
    # the data files aren't present.  We'll catch this below.
    _stopwords = stopwords.words('english')  # type: ignore
    STOPWORDS = set(_stopwords)
    NLTK_AVAILABLE = True
except Exception:
    # Define basic fallback functions
    import re
    NLTK_AVAILABLE = False
    # A minimal set of English stopwords
    STOPWORDS = set([
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has',
        'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was',
        'were', 'will', 'with'
    ])

    def sent_tokenize(text: str) -> List[str]:  # type: ignore
        """Split text into sentences using punctuation as delimiters."""
        # Split on period, exclamation mark or question mark followed by
        # whitespace.  Keep the delimiter by adding it back when splitting.
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def word_tokenize(text: str) -> List[str]:  # type: ignore
        """Split text into words using non‑alphabetic characters as separators."""
        return re.findall(r'[A-Za-z]+', text)


def summarize_text(text: str, max_sentences: int = 2) -> str:
    """Summarise the given text by extracting key sentences.

    Parameters
    ----------
    text: str
        The full text to summarise.
    max_sentences: int, default 2
        The maximum number of sentences to include in the summary.

    Returns
    -------
    str
        A concise summary consisting of the most important sentences.
    """
    sentences: List[str] = sent_tokenize(text)
    if len(sentences) <= max_sentences:
        return ' '.join(sentences)

    # Build frequency table for words
    freq = {}
    for word in word_tokenize(text.lower()):
        if word.lower() in STOPWORDS:
            continue
        freq[word.lower()] = freq.get(word.lower(), 0) + 1

    # Score sentences by the sum of word frequencies
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        words = word_tokenize(sentence.lower())
        if not words:
            continue
        score = 0.0
        for word in words:
            if word.lower() in STOPWORDS:
                continue
            score += freq.get(word.lower(), 0)
        sentence_scores[i] = score / len(words)

    # Select top sentences
    ranked_indices = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
    ranked_indices.sort()  # preserve original order
    return ' '.join(sentences[i] for i in ranked_indices)


def summarize_cluster(cluster: List) -> str:
    """Summarise a cluster of articles by combining their descriptions.

    Parameters
    ----------
    cluster: list of articles
        The articles belonging to the cluster.

    Returns
    -------
    str
        A summary of the cluster.
    """
    if not cluster:
        return ''
    # Concatenate descriptions; fall back to titles if descriptions are missing
    combined_text = ' '.join(
        article.description if article.description else article.title for article in cluster
    )
    return summarize_text(combined_text, max_sentences=2)
