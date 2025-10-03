"""Root package for wallet.dkoded.io.

This package exposes the news and banking packages for import.  It has no side
effects and exists primarily to make relative imports within the repository
work when running scripts from the repository root.
"""

from .packages import news, banks, ui  # noqa: F401
