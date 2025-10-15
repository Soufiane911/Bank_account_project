import random
import json
from pathlib import Path
from typing import Dict
import tkinter as tk
from tkinter import messagebox


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

DATA_FILE = Path(__file__).resolve().parent / "accounts.json"

def account_to_dict(acc: Account) -> dict:
    return {"name": acc.name, "account_number": acc.account_number, "balance": acc.balance}

def dict_to_account(d: dict) -> Account:
    return Account(d["name"], account_number=int(d["account_number"]), balance=int(d["balance"]))

def load_accounts() -> Dict[int, Account]:
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            payload = json.load(f)
        items = payload.get("accounts", {})
        accounts: Dict[int, Account] = {}
        for _, val in items.items():
            acc = dict_to_account(val)
            accounts[int(acc.account_number)] = acc
        return accounts
    except Exception:
        # en cas d'erreur on renvoie un dict vide pour ne pas planter
        return {}

def save_accounts(accounts: Dict[int, Account]) -> None:
    payload = {"accounts": {str(k): account_to_dict(v) for k, v in accounts.items()}}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def seed_defaults(accounts: Dict[int, Account]) -> None:
    """Assure la présence de comptes par défaut si le fichier est vide."""
    changed = False
    if 9502018482 not in accounts:
        accounts[9502018482] = Account("Ross", account_number=9502018482, balance=1350)
        changed = True
    if 1945729572 not in accounts:
        accounts[1945729572] = Account("Rachel", account_number=1945729572, balance=3450)
        changed = True
    if changed:
        save_accounts(accounts)

def launch_gui(accounts: Dict[int, Account]) -> None:
    root = tk.Tk()
    root.title("Banque – Interface")
    root.geometry("520x420")

    root.mainloop()