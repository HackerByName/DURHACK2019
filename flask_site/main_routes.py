from flask_site import *
from flask import render_template, flash, redirect
from flask_site.forms import LoginForm, RegisterForm
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