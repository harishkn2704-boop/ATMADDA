from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid

class TxType(str, Enum):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
    BALANCE_INquiry = "BALANCE"
    MINI_STATEMENT = "MINI_STATEMENT"


@dataclass
class Transaction:
    date: datetime
    type: TxType
    amount: int = 0
    account_number: str = ""
    receipt_id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def print_receipt(self) -> str:
        return (
            f"Receipt #{self.receipt_id}\n"
            f"Date: {self.date.isoformat(timespec='seconds')}\n"
            f"Type: {self.type}\n"
            f"Account: {self.account_number}\n"
            f"Amount: {self.amount}\n"
        )


@dataclass
class Bank:
    name: str
    location: str

    def authorize_account(self, account_number: str, customer_id: str) -> bool:
        return account_number.startswith(customer_id[:4])


@dataclass
class Customer:
    user_id: str
    name: str
    phone: str
    email: str
    pin: int

    def select_options(self, option: str) -> str:
        return option

    def update_information(self, email: Optional[str] = None, phone: Optional[str] = None) -> None:
        if email:
            self.email = email
        if phone:
            self.phone = phone

    def deposit_or_withdraw(self, amount: int) -> int:
        return amount


@dataclass
class Account:
    account_number: str
    bank_name: str
    balance: int
    owner_id: str
    transactions: List[Transaction] = field(default_factory=list)

    def add_tx(self, tx: Transaction) -> None:
        self.transactions.append(tx)

    def mini_statement(self, last_n: int = 5) -> List[Transaction]:
        return self.transactions[-last_n:]


@dataclass
class Checking(Account):
    pass


@dataclass
class Savings(Account):
    pass


@dataclass
class ATM:
    bank_name: str
    location: str
    language: str = "EN"

    def validate_pin(self, input_pin: int, customer: Customer) -> bool:
        return int(input_pin) == int(customer.pin)

    def select_language(self, lang: str) -> None:
        self.language = lang

    def display_options(self) -> List[str]:
        return ["Withdraw", "Deposit", "Balance", "Mini Statement", "Exit"]