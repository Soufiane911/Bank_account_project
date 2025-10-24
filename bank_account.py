import random
import json
from pathlib import Path
from typing import Dict
import tkinter as tk
from tkinter import messagebox


class Account:
    def __init__(self, name: str, account_number: int | None = None, balance: int = 2000, password: str = "1234"):
        self.name = name
        self.account_number = (
            account_number if account_number is not None else random.randint(10**9, 10**10 - 1)
        )
        self.balance = balance
        self.password = password

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
    return {"name": acc.name, "account_number": acc.account_number, "balance": acc.balance, "password": acc.password}


def dict_to_account(d: dict) -> Account:
    return Account(d["name"], account_number=int(d["account_number"]), balance=int(d["balance"]), password=d.get("password", "1234"))


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
        return {}


def save_accounts(accounts: Dict[int, Account]) -> None:
    payload = {"accounts": {str(k): account_to_dict(v) for k, v in accounts.items()}}
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def seed_defaults(accounts: Dict[int, Account]) -> None:
    changed = False
    if 9502018482 not in accounts:
        accounts[9502018482] = Account("Ross", account_number=9502018482, balance=1350, password="ross123")
        changed = True
    if 1945729572 not in accounts:
        accounts[1945729572] = Account("Rachel", account_number=1945729572, balance=3450, password="rachel456")
        changed = True
    if changed:
        save_accounts(accounts)


def launch_gui(accounts: Dict[int, Account]) -> None:
    root = tk.Tk()
    root.title("Banque – Interface Client")
    root.geometry("1280x720")
    root.configure(bg="#dbeafe")  # fond bleu clair

    current = {"acc": None}

    def on_enter(e):
        e.widget["bg"] = "#1e3a8a"  # bleu plus foncé au survol

    def on_leave(e):
        e.widget["bg"] = "#2563eb"  # bleu normal

    def refresh_balance():
        if current["acc"]:
            balance_var.set(f"Solde actuel : {current['acc'].balance} €")

    # ----------- FRAME DE CONNEXION -----------
    login_frame = tk.Frame(root, padx=20, pady=20, bg="#dbeafe")
    tk.Label(login_frame, text="Connexion", font=("Arial", 18, "bold"), bg="#dbeafe", fg="#1e3a8a").pack(pady=(0, 10))

    # Numéro de compte
    account_box = tk.Frame(login_frame, bg="#ffffff", highlightbackground="#93c5fd", highlightthickness=2, padx=10, pady=10)
    tk.Label(account_box, text="Numéro de compte :", bg="#ffffff", fg="#1e3a8a", font=("Arial", 11, "bold")).pack(anchor="w")
    account_entry = tk.Entry(account_box, bg="#f9fafb", fg="black")
    account_entry.pack(fill="x", pady=4)
    account_box.pack(fill="x", pady=10)

    # Mot de passe
    password_box = tk.Frame(login_frame, bg="#ffffff", highlightbackground="#93c5fd", highlightthickness=2, padx=10, pady=10)
    tk.Label(password_box, text="Mot de passe :", bg="#ffffff", fg="#1e3a8a", font=("Arial", 11, "bold")).pack(anchor="w")
    password_entry = tk.Entry(password_box, show="*", bg="#f9fafb", fg="black")
    password_entry.pack(fill="x", pady=4)
    password_box.pack(fill="x", pady=10)

    def styled_button(master, text, command, color="#2563eb"):
        btn = tk.Button(master, text=text, command=command, bg=color, fg="white",
                        font=("Arial", 11, "bold"), relief="ridge", bd=3, padx=10, pady=6)
        if color == "#2563eb":
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        return btn

    styled_button(login_frame, "Se connecter", lambda: do_login(), "#2563eb").pack(pady=10)
    styled_button(login_frame, "Quitter", root.destroy, "#ef4444").pack()

    # ----------- FRAME DE SESSION -----------
    session_frame = tk.Frame(root, padx=20, pady=20, bg="#dbeafe")
    name_var = tk.StringVar(value="")
    balance_var = tk.StringVar(value="Solde : —")
    tk.Label(session_frame, textvariable=name_var, font=("Arial", 14, "bold"), bg="#dbeafe", fg="#1e3a8a").pack(anchor="w")
    tk.Label(session_frame, textvariable=balance_var, font=("Arial", 12), bg="#dbeafe", fg="#111827").pack(anchor="w", pady=(0, 10))

    # --- DÉPÔT ---
    deposit_box = tk.Frame(session_frame, bg="#ffffff", highlightbackground="#93c5fd", highlightthickness=2, padx=10, pady=10)
    tk.Label(deposit_box, text="Montant à déposer :", bg="#ffffff", fg="#1e3a8a", font=("Arial", 11, "bold")).pack(anchor="w")
    deposit_entry = tk.Entry(deposit_box, bg="#f9fafb")
    deposit_entry.pack(anchor="w")
    deposit_entry.insert(0, "0")
    deposit_box.pack(anchor="w", pady=(10, 0))

    def do_deposit():
        if not current["acc"]:
            return
        try:
            amount = int(deposit_entry.get().strip())
            current["acc"].deposit(amount)
            save_accounts(accounts)
            refresh_balance()
            deposit_entry.delete(0, tk.END)
            deposit_entry.insert(0, "0")
            messagebox.showinfo("Succès", f"Dépôt de {amount} € effectué.")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    styled_button(session_frame, "Déposer", do_deposit).pack(anchor="w", pady=(6, 10))

    # --- RETRAIT ---
    withdraw_box = tk.Frame(session_frame, bg="#ffffff", highlightbackground="#93c5fd", highlightthickness=2, padx=10, pady=10)
    tk.Label(withdraw_box, text="Montant à retirer :", bg="#ffffff", fg="#1e3a8a", font=("Arial", 11, "bold")).pack(anchor="w")
    withdraw_entry = tk.Entry(withdraw_box, bg="#f9fafb")
    withdraw_entry.pack(anchor="w")
    withdraw_entry.insert(0, "0")
    withdraw_box.pack(anchor="w", pady=(10, 0))

    def do_withdraw():
        if not current["acc"]:
            return
        try:
            amount = int(withdraw_entry.get().strip())
            current["acc"].withdraw(amount)
            save_accounts(accounts)
            refresh_balance()
            messagebox.showinfo("Succès", f"Retrait de {amount} € effectué.")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    styled_button(session_frame, "Retirer", do_withdraw).pack(anchor="w", pady=(6, 10))

    # --- VIREMENT ---
    send_box = tk.Frame(session_frame, bg="#ffffff", highlightbackground="#93c5fd", highlightthickness=2, padx=10, pady=10)
    tk.Label(send_box, text="Numéro destinataire :", bg="#ffffff", fg="#1e3a8a", font=("Arial", 11, "bold")).pack(anchor="w")
    send_target_entry = tk.Entry(send_box, bg="#f9fafb")
    send_target_entry.pack(anchor="w", pady=(0, 6))
    tk.Label(send_box, text="Montant à envoyer :", bg="#ffffff", fg="#1e3a8a", font=("Arial", 11, "bold")).pack(anchor="w")
    send_amount_entry = tk.Entry(send_box, bg="#f9fafb")
    send_amount_entry.pack(anchor="w")
    send_amount_entry.insert(0, "0")
    send_box.pack(anchor="w", pady=(10, 0))

    def do_send():
        if not current["acc"]:
            return
        try:
            target_num = int(send_target_entry.get().strip())
            amount = int(send_amount_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir des nombres valides.")
            return
        target = accounts.get(target_num)
        if not target:
            messagebox.showerror("Erreur", "Compte destinataire introuvable.")
            return
        try:
            current["acc"].withdraw(amount)
            target.deposit(amount)
            save_accounts(accounts)
            refresh_balance()
            messagebox.showinfo("Succès", f"Virement de {amount} € vers le compte {target.account_number}.")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    styled_button(session_frame, "Envoyer", do_send).pack(anchor="w", pady=(6, 10))

    # --- DÉCONNEXION ---
    def do_logout():
        current["acc"] = None
        account_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        session_frame.pack_forget()
        login_frame.pack(fill="both", expand=True, padx=30, pady=30)

    styled_button(session_frame, "Déconnexion", do_logout, "#ef4444").pack(anchor="w", pady=(12, 0))
    styled_button(session_frame, "Quitter", root.destroy, "#ef4444").pack(anchor="w", pady=(6, 0))

    # --- Connexion ---
    def do_login():
        raw_account = account_entry.get().strip()
        raw_password = password_entry.get().strip()
        try:
            num = int(raw_account)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir un numéro valide.")
            return
        acc = accounts.get(num)
        if not acc:
            messagebox.showerror("Erreur", "Compte introuvable.")
            return
        if acc.password != raw_password:
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
            return
        current["acc"] = acc
        name_var.set(f"Titulaire : {acc.name} | Compte : {acc.account_number}")
        refresh_balance()
        login_frame.pack_forget()
        session_frame.pack(fill="both", expand=True, padx=30, pady=30)

    login_frame.pack(fill="both", expand=True, padx=30, pady=30)
    root.mainloop()


def main() -> None:
    accounts = load_accounts()
    seed_defaults(accounts)
    launch_gui(accounts)


if __name__ == "__main__":
    accounts = load_accounts()
    seed_defaults(accounts)
    launch_gui(accounts)
