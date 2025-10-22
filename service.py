from __future__ import annotations
from datetime import datetime
from typing import Tuple, List
from domain import (
    ATM, Bank, Customer, Account, Checking, Savings, Transaction, TxType
)
from repo import InMemoryRepo


class ATMService:
    def __init__(self, atm: ATM, bank: Bank, repo: InMemoryRepo):
        self.atm = atm
        self.bank = bank
        self.repo = repo

    # Card + PIN
    def insert_card(self, user_id: str) -> Customer:
        cust = self.repo.get_customer(user_id)
        if not cust:
            raise ValueError("Card not recognized")
        return cust

    def validate_pin(self, customer: Customer, pin: int) -> bool:
        return self.atm.validate_pin(pin, customer)

    # Account selection
    def list_accounts(self, customer: Customer):
        return self.repo.get_accounts_by_owner(customer.user_id)

    # Core operations
    def withdraw(self, account: Account, amount: int) -> Tuple[int, Transaction]:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > account.balance:
            raise ValueError("Insufficient funds")
        account.balance -= amount
        tx = Transaction(
            date=datetime.now(),
            type=TxType.WITHDRAW,
            amount=amount,
            account_number=account.account_number,
        )
        account.add_tx(tx)
        return account.balance, tx

    def deposit(self, account: Account, amount: int) -> Tuple[int, Transaction]:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        account.balance += amount
        tx = Transaction(
            date=datetime.now(),
            type=TxType.DEPOSIT,
            amount=amount,
            account_number=account.account_number,
        )
        account.add_tx(tx)
        return account.balance, tx

    def balance(self, account: Account) -> Tuple[int, Transaction]:
        tx = Transaction(
            date=datetime.now(),
            type=TxType.BALANCE_INquiry,
            amount=0,
            account_number=account.account_number,
        )
        account.add_tx(tx)
        return account.balance, tx

    def mini_statement(self, account: Account, last_n: int = 5) -> List[Transaction]:
        tx = Transaction(
            date=datetime.now(),
            type=TxType.MINI_STATEMENT,
            amount=0,
            account_number=account.account_number,
        )
        account.add_tx(tx)
        return account.mini_statement(last_n)


# Seed utility
def seed_demo(repo: InMemoryRepo) -> Tuple[Bank, ATM, Customer, Account, Account]:
    bank = Bank(name="Perplexity Bank", location="Main Street")
    atm = ATM(bank_name=bank.name, location="Campus Lobby")

    cust = Customer(
        user_id="22MIC0124",
        name="HARISH",
        phone="9361230329",
        email="harish@gmail.com",
        pin=2704,
    )
    repo.add_customer(cust)

    chk = Checking(
        account_number="22MIC0124-CHK-001",
        bank_name=bank.name,
        balance=10_000,
        owner_id=cust.user_id,
    )
    sav = Savings(
        account_number="22MIC0124-SAV-001",
        bank_name=bank.name,
        balance=25_000,
        owner_id=cust.user_id,
    )
    repo.add_account(chk)
    repo.add_account(sav)

    return bank, atm, cust, chk, sav