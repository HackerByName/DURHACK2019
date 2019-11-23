from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask("test")
bcrypt = Bcrypt(app)

class User:
    @staticmethod
    def create_new_user(first_name, last_name, email, password):
        accounts = ["personal"]
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        print(hashed)
        #add it to the database
        id = 0
        user = User(id, first_name, last_name, email, accounts)
        return user

    def __init__(self, id, first_name, last_name, email, accounts):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.accounts = accounts

    def create_account(self, name):
        new_account = Account.create_new_account(id, name)

class Account:
    @staticmethod
    def create_new_account(owner_id, account_name, time_created, initial_balance):
        account = Account(owner_id, account_name, time_created, initial_balance)
        #add it to the database here

    def __init__(self, id, owner_id, account_name, time_created, balance):
        self.id = id
        self.owner_id = owner_id
        self.account_name = account_name
        self.time_created = time_created
        self.balance = balance

    def add_transacation(self):
        pass

    def get_transactions(self):
        pass

app = Flask("app")

def login(email, password):
    #get the user's record from MongoDB
    #check hash
    #login if password works
    pass

user = User.create_new_user("finlay", "boyle", "test", "a")
