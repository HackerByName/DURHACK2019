from pymongo import MongoClient
from pprint import pprint
from time import time
from flask_site import student_records

"""

MAIN FUNCTIONALITY:

1) insertNewUser() -> Adds new user to database
2) addAccountToUser() -> Adds account to user
3) newTransaction() -> Adds transaction to database with reference to user
4) getBalance() -> Gets balance of user
5) printAllRecords() -> prints all records in a collection of database

"""

class MongoDatabase:
    @staticmethod
    def print_all_records(records):
        pprint(list(records.find()))

    @staticmethod
    def insert_new_user(records, first_name, last_name, email, password):
        newUser = {
            'first_name' : str(first_name),
            'last_name' : str(last_name),
            'email' : str(email),
            'password' : str(password),
            'accounts' : []
        }

        user_id = records.insert_one(newUser)

        MongoDatabase.add_account_to_user(student_records, first_name, last_name, "personal", 0)

    @staticmethod
    def create_new_transaction(transaction_records, student_id, account_name, money_spent):
        newTransaction = {
            'student_id' : str(student_id),
            'account_name' : str(account_name),
            'money_spent' : f"{money_spent:.2f}",
            'date'  : time()
        }

        transaction_records.insert_one(newTransaction)

    @staticmethod
    def get_account_index_from_name(account_array, account_name):
        for i in range(0, len(account_array)):
            if (account_array[i]['account_name'] == account_name):
                return i
        return -1

    @staticmethod
    def add_account_to_user(records, first_name, last_name, account_name, initial_balance):
        user = MongoDatabase.get_student(records, first_name, last_name)
        user_id = MongoDatabase.get_student_id(records, first_name, last_name)
        accountArray = user['accounts']
        accountArray.append({
            'account_name' : account_name,
            'balance'   :   initial_balance,
            'date_created'  : time()
        })
        newDictionary = {'accounts' : accountArray}
        records.update({'_id':user_id}, {"$set": newDictionary}, upsert=False)

    @staticmethod
    def get_student(records, first_name, last_name):
        return records.find_one({"first_name":str(first_name),"last_name":str(last_name)})

    @staticmethod
    def get_student_id(records, first_name, last_name):
        return MongoDatabase.get_student(records, first_name, last_name)['_id']

    @staticmethod
    def find_record(records, filter):
        return records.find_one(filter)

    @staticmethod
    def get_balance(student_records, transaction_records, student_id, account_name):
        user = student_records.find_one({"_id":student_id})
        currentBalance = float(user['accounts'][MongoDatabase.get_account_index_from_name(user['accounts'], account_name)]['balance'])

        transactionList = []
        transactionCursor = transaction_records.find({"student_id":str(student_id)})
        for transaction in transactionCursor:
            if (transaction['account_name'] == account_name):
                currentBalance -= float(transaction['money_spent'])
        return f"{currentBalance:.2f}"

    @staticmethod
    def yield_balance(student_records, transaction_records, student_id, account_name):
        user = student_records.find_one({"_id":student_id})
        currentBalance = float(user['accounts'][MongoDatabase.get_account_index_from_name(user['accounts'], account_name)]['balance'])

        yield currentBalance

        transactionList = []
        transactionCursor = transaction_records.find({"student_id":str(student_id)})
        for transaction in transactionCursor:
            if (transaction['account_name'] == account_name):
                currentBalance -= float(transaction['money_spent'])
                yield currentBalance

        yield currentBalance


#insertNewUser(student_records, 'Bob', 'Smith', 'bobsmith@gmail.com', 'yyyyyy', )
#addAccountToUser(student_records, 'Bob', 'Smith', 'public', 500)
#addAccountToUser(student_records, 'Bob', 'Smith', 'private', 1000)
#newTransaction(transaction_records, getStudentID(student_records, 'Bob', 'Smith'), 'private', 100)
#newTransaction(transaction_records, getStudentID(student_records, 'Bob', 'Smith'), 'private', 100)


#printAllRecords(student_records)
#printAllRecords(transaction_records)
#print(getBalance(student_records, transaction_records, getStudentID(student_records, 'Bob', 'Smith'), 'private'))
