"""Provider‑agnostic banking adapters.

This package defines a minimal interface for interacting with banking APIs and
includes stub implementations for Plaid, TrueLayer and Tink.  Each provider
class implements the same methods, enabling the rest of the application to
interact with bank data without caring about the underlying provider.
"""

from .base import BankProvider  # noqa: F401
from .providers import PlaidProvider, TrueLayerProvider, TinkProvider, DemoBankProvider  # noqa: F401
