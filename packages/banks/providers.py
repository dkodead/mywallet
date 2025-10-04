"""Stub implementations of bank providers.

These providers return static data for demonstration purposes.  In a real
deployment, each class would call the corresponding API (e.g. Plaid, TrueLayer
or Tink) using appropriate credentials and return live data.
"""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
import random

from .base import BankProvider


class DemoBankProvider(BankProvider):
    """A simple provider that returns hard‑coded balances and transactions."""

    def __init__(self) -> None:
        self.accounts = [
            {
                'account_id': 'acc-001',
                'account_type': 'checking',
                'currency': 'EUR',
                'name': 'Main Checking',
            },
            {
                'account_id': 'acc-002',
                'account_type': 'savings',
                'currency': 'EUR',
                'name': 'Emergency Savings',
            },
        ]

    def get_balances(self) -> List[Dict[str, Any]]:
        return [
            {
                'account_id': 'acc-001',
                'currency': 'EUR',
                'amount': 2450.75,
                'last_updated': datetime.utcnow().isoformat(),
            },
            {
                'account_id': 'acc-002',
                'currency': 'EUR',
                'amount': 10000.00,
                'last_updated': datetime.utcnow().isoformat(),
            },
        ]

    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        # Generate some pseudo transactions for the last few days
        transactions: List[Dict[str, Any]] = []
        for i in range(5):
            transactions.append({
                'id': f'tx-{account_id}-{i}',
                'date': (datetime.utcnow().date()).isoformat(),
                'amount': round(random.uniform(-100, 100), 2),
                'description': f'Demo transaction {i}',
                'account_id': account_id,
            })
        return transactions

    def get_accounts(self) -> List[Dict[str, Any]]:
        return self.accounts


class PlaidProvider(BankProvider):
    """Placeholder for a Plaid banking provider."""

    def get_balances(self) -> List[Dict[str, Any]]:
        # TODO: integrate Plaid API
        return []

    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        return []

    def get_accounts(self) -> List[Dict[str, Any]]:
        return []


class TrueLayerProvider(BankProvider):
    """Placeholder for a TrueLayer banking provider."""

    def get_balances(self) -> List[Dict[str, Any]]:
        # TODO: integrate TrueLayer API
        return []

    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        return []

    def get_accounts(self) -> List[Dict[str, Any]]:
        return []


class TinkProvider(BankProvider):
    """Placeholder for a Tink banking provider."""

    def get_balances(self) -> List[Dict[str, Any]]:
        # TODO: integrate Tink API
        return []

    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        return []

    def get_accounts(self) -> List[Dict[str, Any]]:
        return []
