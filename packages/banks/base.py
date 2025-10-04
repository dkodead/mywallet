"""Base classes for banking providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BankProvider(ABC):
    """Abstract base class for banking providers.

    Subclasses must implement methods to retrieve account balances,
    transaction history and other banking information.  This interface can
    accommodate both synchronous and asynchronous providers depending on the
    needs of the application.
    """

    @abstractmethod
    def get_balances(self) -> List[Dict[str, Any]]:
        """Return a list of account balance objects.

        Each balance should include at least an ``account_id``, ``currency`` and
        ``amount``.  Additional fields are provider‑specific.
        """

    @abstractmethod
    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        """Return a list of recent transactions for the given account.

        Each transaction should include a date, amount, description and any
        other relevant metadata.
        """

    @abstractmethod
    def get_accounts(self) -> List[Dict[str, Any]]:
        """Return a list of accounts available to the user."""
