from flask_site import *
from flask import render_template, flash, redirect
from flask_site.forms import AddTransactionForm
from .mongo import MongoDatabase
from .helper import Verifications, User

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/index")

    balance_history = session["user"].generate_account_history("personal")
    balance = [balance_history[k] for k in balance_history]

    return render_template("dashboard.html", title="Dashboard", user=(session["user"] if "user" in session else None), balance_history=balance)

@app.route("/accounts")
def accounts():
    return render_template("accounts.html", title="Accounts", user=(session["user"] if "user" in session else None))

@app.route("/history")
def history():
    return render_template("history.html", title="History", user=(session["user"] if "user" in session else None))

@app.route("/settings")
def settings():
    return render_template("settings.html", title="Settings", user=(session["user"] if "user" in session else None))

@app.route("/user")
def user():
    return render_template("user.html", title="User Settings", user=(session["user"] if "user" in session else None))

@app.route("/add", methods=["GET"])
def add():
    form = AddTransactionForm()
    return render_template("add.html", title="Add Transaction", user=(session["user"] if "user" in session else None), form=form)

@app.route("/add", methods=["POST"])
def process_add():
    form = AddTransactionForm()

    if form.validate_on_submit():
        direction = 1 if form.direction.data == "in" else -1
        amount = form.amount.data
        notes = form.notes.data
        MongoDatabase.insert_new_transacation(session["user"].id, session["account"], direction * amount, notes)

        return redirect("/history")

    return render_template("add.html", title="Add Transaction", user=(session["user"] if "user" in session else None), form=form)
