from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_session import MongoDBSessionInterface, Session
from config import Config
from pymongo import MongoClient
from pprint import pprint
from time import time

database_client = MongoClient("mongodb+srv://max:Password123@studentfinancecluster-hl4cr.mongodb.net/test?retryWrites=true&w=majority")
database_student = database_client.get_database("student_db")
student_records = database_student.students
transaction_records = database_student.transactions
accounts_records = database_student.accounts

app = Flask(__name__)

app.config["SESSION_MONGODB"] = database_client
app.config["SESSION_MONGODB_DB"] = "student_db"
app.config["SESSION_MONGODB_COLLECT"] = "sessions"
app.config["SECRET_KEY"] = "this_isnt_very_secret"
app.config["SESSION_TYPE"] = "mongodb"

bcrypt = Bcrypt(app)
Session(app)

from flask_site import routes
