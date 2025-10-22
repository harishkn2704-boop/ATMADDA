from __future__ import annotations
from typing import Dict, Optional
from domain import Customer, Account


class InMemoryRepo:
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.accounts: Dict[str, Account] = {}

    # Customer
    def add_customer(self, c: Customer) -> None:
        self.customers[c.user_id] = c

    def get_customer(self, user_id: str) -> Optional[Customer]:
        return self.customers.get(user_id)

    # Account
    def add_account(self, a: Account) -> None:
        self.accounts[a.account_number] = a

    def get_account(self, account_number: str) -> Optional[Account]:
        return self.accounts.get(account_number)

    def get_accounts_by_owner(self, user_id: str):
        return [a for a in self.accounts.values() if a.owner_id == user_id]