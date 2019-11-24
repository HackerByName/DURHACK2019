from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, FloatField, TimeField
from wtforms.fields.html5 import DateField
from datetime import datetime
from wtforms.validators import DataRequired, Email, Required
from flask import Flask, session

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Register')

class UserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

class PasswordForm(FlaskForm):
    password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddTransactionForm(FlaskForm):
    direction = RadioField("In / Out", choices=[("in", "In"), ("out", "Out")], validators=[DataRequired()])
    amount = FloatField("Amount", validators=[DataRequired()])
    when_date = DateField("Date", default=datetime.now(), validators=[DataRequired()])
    when_time = TimeField("Time", default=datetime.now().time(), validators=[DataRequired()], format="%H:%M")
    notes = TextAreaField("Notes", validators=[DataRequired()])
    retailer = StringField("Retailer", validators=[DataRequired()])
    submit = SubmitField("Add Transaction")

class UniversityBudgetForm(FlaskForm):
    university_budget = StringField("University Budget", validators=[DataRequired()])
    submit = SubmitField("Set Budget")

class PersonalBudgetForm(FlaskForm):
    personal_budget = StringField("Personal Budget", validators=[DataRequired()])
    submit = SubmitField("Set Budget")
