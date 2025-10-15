import random

class Account:
    def __init__(self, name: str, account_number: int | None = None, balance: int = 2000):
        self.name = name
        self.account_number = (
            account_number if account_number is not None else random.randint(10**9, 10**10 - 1)
        )
        self.balance = balance

    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        self.balance -= amount