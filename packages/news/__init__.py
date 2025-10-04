"""Top‑level package for the news engine.

This package exposes a single entry point, :func:`run_pipeline`, which ingests
articles, clusters them, scores them for importance and produces a summary for
each topic.  See `packages/news/pipeline.py` for the implementation.
"""

from .pipeline import run_pipeline  # noqa: F401
