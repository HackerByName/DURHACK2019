from flask_site import *

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
         record["email"], record["accounts"])

    def __init__(self, id, first_name, last_name, email, accounts):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.accounts = accounts
