from flask import Flask
from flask_bcrypt import Bcrypt
from config import Config
from pymongo import MongoClient
from pprint import pprint
from time import time

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object(Config)

database_client = MongoClient("mongodb+srv://max:Password123@studentfinancecluster-hl4cr.mongodb.net/test?retryWrites=true&w=majority")
database_student = database_client.get_database("student_db")
student_records = database_student.students
transaction_records = database_student.transactions
accounts_records = database_student.accounts

from flask_site import routes
