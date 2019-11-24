from pymongo import MongoClient
from time import time
from flask_site import student_records, transaction_records

class MongoDatabase:
    @staticmethod
    def insert_new_user(first_name, last_name, email, password):
        new_user = {
            "first_name": str(first_name),
            "last_name": str(last_name),
            "email": str(email),
            "password": str(password),
            "accounts": [{
                "name": "personal",
                "created": time()
            }],
            "budgets" : {
                "personal" : 0,
                "university" : 0
            }
        }

        student_records.insert_one(new_user)

    @staticmethod
    def insert_new_transacation(student_id, account_name, amount, notes, retailer, when):
        new_transaction = {
            "student_id": str(student_id),
            "account_name": str(account_name),
            "amount": f"{amount:.2f}",
            "date": when,
            "notes": notes,
            "retailer": retailer
        }

        transaction_records.insert_one(new_transaction)

    @staticmethod
    def update_student(student_id, update_dictionary):
        student_records.update({"_id": student_id}, update_dictionary, upsert=False)

    @staticmethod
    def find_records(records, filter):
        return records.find(filter)

    @staticmethod
    def find_record(records, filter):
        return records.find_one(filter)

    @staticmethod
    def get_balance(student_records, transaction_records, student_id):
        user = student_records.find_one({"_id":student_id})
        currentBalance = 0

        transactionList = []
        transactionCursor = transaction_records.find({"student_id":str(student_id)})
        for transaction in transactionCursor:
            currentBalance += float(transaction['amount'])
        return f"{currentBalance:.2f}"
