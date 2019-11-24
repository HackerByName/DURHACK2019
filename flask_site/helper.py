from flask_site import *
from .mongo import MongoDatabase
from time import time

class Verifications:
    @staticmethod
    def is_logged_in():
        return "user" in session

    def logout():
        if Verifications.is_logged_in():
            session.pop("user", None)

class User:
    @staticmethod
    def from_record(record):
        return User(record["_id"], record["first_name"], record["last_name"],
         record["email"], record["budgets"])

    def __init__(self, id, first_name, last_name, email, budgets):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.budgets = budgets

    def create_account(self, account):
        accounts = self.get_accounts()

        if account in accounts:
            #Can't make this
            return False

        accounts.append({
            "name": account,
            "created": time()
        })

        updateable = {'accounts': accounts}
        MongoDatabase.update_student(self.id, {"$set": updateable})

    def get_accounts(self):
        user_record = MongoDatabase.find_records(student_records, {"_id": self.id})
        return user_record[0]["accounts"]

    def get_account_transacations(self, account):
        transactions = MongoDatabase.find_records(transaction_records, {"student_id": str(self.id), "account_name": account})
        return transactions

    def generate_account_history(self, account):
        transactions = self.get_account_transacations(account)
        transactions = [x for x in transactions]
        transactions = sorted(transactions, key=lambda x: x["date"])
        balance = 0
        account_history = {}

        for record in transactions:
            date = record["date"]
            notes = record["notes"]
            retailer = record["retailer"]
            balance += float(record["amount"])

            #print(balance, record["amount"])

            account_history[date] = {
                "date": date,
                "balance": balance,
                "notes": notes,
                "retailer": retailer,
                "amount": float(record["amount"])
            }

        #print("Acc_history:", account_history)
        return account_history
