from flask_site import *
from flask import render_template, flash, redirect, Response
from flask_site.forms import UserForm, PasswordForm, AddTransactionForm
from .mongo import MongoDatabase
from .helper import Verifications, User
from datetime import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import io
import base64

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/index")

    balance_history = session["user"].generate_account_history("personal")
    balance = [balance_history[k] for k in balance_history]
    curr_balance = MongoDatabase.get_balance(student_records, transaction_records, session["user"].id)

    return render_template("dashboard.html", title="Dashboard", user=(session["user"] if "user" in session else None), balance_history=balance, my_balance=curr_balance)

@app.route("/dashboard_basic_graph.png")
def generate_basic_graph():
    balance_history = session["user"].generate_account_history("personal")
    balances = [balance_history[k] for k in balance_history]

    figure = create_basic_visual(balances)
    output = io.BytesIO()
    FigureCanvas(figure).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')

def create_basic_visual(balances):
    figure = Figure()
    axis = figure.add_subplot(1, 1, 1)
    #figure.ylabel("Balance (£)")
    #figure.xlabel("Date")
    x_points = []
    y_points = []

    for element in balances:
        x_points.append(element["date"])
        y_points.append(element["balance"])

    minimum = min(x_points)
    x_points = [(x - minimum) for x in x_points]
    axis.plot(x_points, y_points)
    return figure

@app.route("/dashboard_pie_chart.png")
def generate_pie_chart(bType):
    balance = 500
    budget = 1000
    
    img = io.BytesIO()
    
    labels = 'Budget', 'Leftover'
    sizes = [balance, budget-balance]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=none, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')

    figure = ax1
    plt.plot(figure)
    plt.savefig(img, format='png')
    FigureCanvas(figure).print_png(output)
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

@app.route("/budgets")
def budgets():
    return render_template("budgets.html", title="Budgeting", user=(session["user"] if "user" in session else None))

@app.route("/history")
def history():
    acc_history = session["user"].generate_account_history(session["account"])
    print(acc_history)
    his = []

    for k in sorted(acc_history, reverse=True):
        new_dict = {"date": datetime.utcfromtimestamp(acc_history[k]["date"]).strftime('%Y-%m-%d %H:%M:%S'),
        "balance": f'{acc_history[k]["balance"]:.2f}', "notes": acc_history[k]["notes"], "amount": f'{acc_history[k]["amount"]:.2f}', "retailer": acc_history[k]["retailer"]}
        his.append(new_dict)

    return render_template("history.html", title="History", user=(session["user"] if "user" in session else None), transaction_history=his)

@app.route("/settings")
def settings():
    return render_template("settings.html", title="Settings", user=(session["user"] if "user" in session else None))

@app.route("/user")
def user():
    return render_template("user.html", title="User Settings", user=(session["user"] if "user" in session else None))

@app.route("/user/edit")
def userEdit():
    user_form = UserForm()
    return render_template("user_edit.html", form=user_form, title="User Edit", user=(session["user"] if "user" in session else None))

@app.route("/user/change_password")
def userEditPassword():
    pass_form = PasswordForm()
    return render_template("user_change_password.html", form=pass_form, title="User Edit", user=(session["user"] if "user" in session else None))

@app.route("/setUniversityBudget")
def uniBudget():
    budget_form = UserForm()
    return render_template("setUniversityBudget.html", form=budget_form, title="Uni Budget", user=(session["user"] if "user" in session else None))

@app.route("/setPersonalBudget")
def personalBudget():
    budget_form = UserForm()
    return render_template("setPersonalBudget.html", form=budget_form, title="Personal Budget", user=(session["user"] if "user" in session else None))

@app.route("/add", methods=["GET"])
def add():
    form = AddTransactionForm()
    return render_template("add.html", title="Add Transaction", user=(session["user"] if "user" in session else None), form=form)

@app.route("/add", methods=["POST"])
def process_add():
    form = AddTransactionForm()

    if form.validate_on_submit():
        print(form.direction.data)
        direction = 1 if form.direction.data == 'in' else -1
        print(direction)
        amount = int(form.amount.data)
        notes = form.notes.data
        retailer = form.retailer.data
        MongoDatabase.insert_new_transacation(session["user"].id, session["account"], direction * amount, notes, retailer)

        return redirect("/history")

    return render_template("add.html", title="Add Transaction", user=(session["user"] if "user" in session else None), form=form)
