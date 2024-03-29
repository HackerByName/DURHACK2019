from flask_site import *
from flask import render_template, flash, redirect, Response
from flask_site.forms import *
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

    this_id = session["user"].id
    session["user"] = User.from_record(MongoDatabase.find_record(student_records, {"_id": this_id}))

    balance_history = session["user"].generate_account_history("personal")
    balance = [balance_history[k] for k in balance_history]
    curr_balance = MongoDatabase.get_balance(student_records, transaction_records, session["user"].id)

    return render_template("dashboard.html", title="Dashboard", user=(session["user"] if "user" in session else None), balance_history=balance, my_balance=curr_balance)

@app.route("/dashboard_basic_graph.png")
def generate_basic_graph():
    balance_history = session["user"].generate_account_history("personal")
    balances = [balance_history[k] for k in balance_history]

    if len(balances) == 0:
        return None

    figure = create_basic_visual(balances)
    output = io.BytesIO()
    FigureCanvas(figure).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')

def create_basic_visual(balances):
    figure = Figure()
    axis = figure.add_subplot(1, 1, 1)
    axis.set_ylabel("Balance (£)")
    axis.set_xlabel("Date")

    x_points = []
    y_points = []

    for element in balances:
        x_points.append(element["date"])
        y_points.append(element["balance"])

    minimum = min(x_points)
    x_points = [datetime.utcfromtimestamp(x).strftime('%d/%m/%Y %H:%M') for x in x_points]
    axis.plot(x_points, y_points)
    figure.autofmt_xdate()
    figure.tight_layout()
    return figure

@app.route("/dashboard_pie_chart.png")
def generate_pie_chart():
    balance = float(MongoDatabase.get_balance(student_records, transaction_records, session["user"].id))
    personal_budget = float(session['user'].budgets['personal'])
    uni_budget = float(session['user'].budgets['university'])

    if balance == 0:
        return None

    img = io.BytesIO()

    figure = Figure()
    ax1 = figure.add_subplot(1, 1, 1)
    labels = ['Remaining', 'University Budget', 'Personal Budget']
    sizes = [balance - personal_budget - uni_budget, uni_budget, personal_budget]
    ax1.pie(sizes, explode=None, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')
    FigureCanvas(figure).print_png(img)
    return Response(img.getvalue(), mimetype='image/png')

@app.route("/dashboard_retailer_breakdown.png")
def generate_retailer_breakdown():
    balance_history = session["user"].generate_account_history("personal")
    balances = [balance_history[k] for k in balance_history]

    if len(balances) == 0:
        return None

    retailers = {}

    for record in balances:
        if record["retailer"] in retailers:
            retailers[record["retailer"]] += record["amount"]
        else:
            retailers[record["retailer"]] = record["amount"]

    labels = []
    chunks = []

    for k in retailers:
        if retailers[k] >= 0:
            continue

        labels.append(k + ": £" + f'{retailers[k]:.2f}')
        chunks.append(-retailers[k])

    print(labels)
    print(chunks)

    img = io.BytesIO()
    figure = Figure()
    axis = figure.add_subplot(1, 1, 1)
    axis.pie(chunks, explode=None, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    axis.axis("equal")
    FigureCanvas(figure).print_png(img)
    return Response(img.getvalue(), mimetype='image/png')

@app.route("/dashboard_income_breakdown.png")
def generate_income_breakdown():
    balance_history = session["user"].generate_account_history("personal")
    balances = [balance_history[k] for k in balance_history]

    if len(balances) == 0:
        return None
        
    retailers = {}

    for record in balances:
        if record["retailer"] in retailers:
            retailers[record["retailer"]] += record["amount"]
        else:
            retailers[record["retailer"]] = record["amount"]

    labels = []
    chunks = []

    for k in retailers:
        if retailers[k] <= 0:
            continue

        labels.append(k + ": £" + f'{retailers[k]:.2f}')
        chunks.append(retailers[k])

    print(labels)
    print(chunks)

    img = io.BytesIO()
    figure = Figure()
    axis = figure.add_subplot(1, 1, 1)
    axis.pie(chunks, explode=None, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    axis.axis("equal")
    FigureCanvas(figure).print_png(img)
    return Response(img.getvalue(), mimetype='image/png')

@app.route("/budgets")
def budgets():
    curr_balance = MongoDatabase.get_balance(student_records, transaction_records, session["user"].id)
    print(curr_balance)
    return render_template("budgets.html", title="Budgeting", user=(session["user"] if "user" in session else None), my_balance=curr_balance)

@app.route("/history")
def history():
    acc_history = session["user"].generate_account_history(session["account"])
    #print(acc_history)
    his = []

    for k in sorted(acc_history, reverse=True):
        new_dict = {"date": datetime.utcfromtimestamp(acc_history[k]["date"]).strftime('%d/%m/%Y %H:%M'),
        "balance": f'{acc_history[k]["balance"]:.2f}', "notes": acc_history[k]["notes"], "amount": f'{acc_history[k]["amount"]:.2f}', "retailer": acc_history[k]["retailer"]}
        his.append(new_dict)

    return render_template("history.html", title="History", user=(session["user"] if "user" in session else None), transaction_history=his)

@app.route("/settings")
def settings():
    return render_template("settings.html", title="Settings", user=(session["user"] if "user" in session else None))

@app.route("/user")
def user():
    return render_template("user.html", title="User Settings", user=(session["user"] if "user" in session else None))

@app.route("/user/edit", methods=["GET"])
def userEdit():
    user_form = UserForm()
    return render_template("user_edit.html", form=user_form, title="User Edit", user=(session["user"] if "user" in session else None))

@app.route("/user/change_password", methods=["GET"])
def userEditPassword():
    pass_form = PasswordForm()
    return render_template("user_change_password.html", form=pass_form, title="User Edit", user=(session["user"] if "user" in session else None))

@app.route("/user/change_password", methods=["POST"])
@app.route("/user/edit", methods=["POST"])
def doesnt_exist():
    return render_template("not_implemented.html", title="Not Implemented", user=(session["user"] if "user" in session else None))

@app.route("/setUniversityBudget", methods=["GET"])
def uniBudget():
    budget_form = UniversityBudgetForm()
    return render_template("setUniversityBudget.html", form=budget_form, title="Uni Budget", user=(session["user"] if "user" in session else None))

@app.route("/setUniversityBudget", methods=["POST"])
def uniBudgetPost():

    form = UniversityBudgetForm()

    if form.validate_on_submit():
        user = MongoDatabase.find_record(student_records, {"_id":session["user"].id})
        university_budget = int(form.university_budget.data)
        user['budgets']['university'] = university_budget
        dictionary = {"$set": user}
        MongoDatabase.update_student(session["user"].id, dictionary)

        return redirect("/dashboard")
    return render_template("setUniversityBudget.html", form=budget_form, title="Uni Budget", user=(session["user"] if "user" in session else None))

@app.route("/setPersonalBudget", methods=["GET"])
def personalBudget():
    budget_form = PersonalBudgetForm()
    return render_template("setPersonalBudget.html", form=budget_form, title="Personal Budget", user=(session["user"] if "user" in session else None))

@app.route("/setPersonalBudget", methods=["POST"])
def personalBudgetPost():

    form = PersonalBudgetForm()

    if form.validate_on_submit():
        user = MongoDatabase.find_record(student_records, {"_id":session["user"].id})
        personal_budget = int(form.personal_budget.data)
        user['budgets']['personal'] = personal_budget
        dictionary = {"$set": user}
        MongoDatabase.update_student(session["user"].id, dictionary)

        return redirect("/dashboard")
    return render_template("setPersonalBudget.html", form=budget_form, title="Personal Budget", user=(session["user"] if "user" in session else None))

@app.route("/add", methods=["GET"])
def add():
    form = AddTransactionForm()
    return render_template("add.html", title="Add Transaction", user=(session["user"] if "user" in session else None), form=form)

@app.route("/add", methods=["POST"])
def process_add():
    form = AddTransactionForm()

    if form.validate_on_submit():
        direction = 1 if form.direction.data == 'in' else -1
        amount = int(form.amount.data)
        notes = form.notes.data
        retailer = form.retailer.data
        seconds = datetime.now().strftime('%S')
        w = str(form.when_date.data) + " " + str(form.when_time.data)
        w = w[:-2] + str(seconds)
        when = datetime.timestamp(datetime.strptime(w, "%Y-%m-%d %H:%M:%S"))
        print(when)

        MongoDatabase.insert_new_transacation(session["user"].id, session["account"], direction * amount, notes, retailer, when)

        return redirect("/history")

    return render_template("add.html", title="Add Transaction", user=(session["user"] if "user" in session else None), form=form)
