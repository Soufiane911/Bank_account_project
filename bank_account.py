import random

class Account:
    def __init__(self, name: str, account_number: int | None = None, balance: int = 2000):
        self.name = name
        self.account_number = (
            account_number if account_number is not None else random.randint(10**9, 10**10 - 1)
        )
        self.balance = balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être positif")
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être positif")
        if amount > self.balance:
            raise ValueError("Fonds insuffisants")
        self.balance -= amount

    def dump(self) -> None:
        print(f"{self.name}, {self.account_number}, {self.balance}")

