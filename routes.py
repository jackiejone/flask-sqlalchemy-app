# Importing libraries
import os
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, validators, SubmitField, ValidationError
from flask_wtf import FlaskForm
import forms

# declaring database location
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "backpack_database.db"))

# Declaring app, database file, and secret key
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = '6342742364SSDAYDG^T&gyu&&*&sdghhs&*&87'

db = SQLAlchemy(app)

# Defining database model
class Backpack(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    item = db.Column(db.String(80), unique=True, nullable=False)

db.create_all()

# Home page route
@app.route("/", methods=["GET", "POST"])
def home():
    form_add = forms.Add() # Defining forms
    form_delete = forms.Delete()
    if form_add.validate_on_submit(): # Adding item into database,
        item_name = form_add.item.data.strip()
        item = Backpack(item=item_name, amount=1)
        database_item = Backpack.query.filter_by(item=item_name).first()
        if database_item == None: # checking if item is in database
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        else:
            database_item.amount = database_item.amount + 1 # Incrementing item amount if item is in database
            db.session.commit()
            return redirect('/')
    backpack_items = Backpack.query.all()
    return render_template("home.html", backpack_items=backpack_items, form_add=form_add, form_delete=form_delete)

# Route for delete function
@app.route('/delete', methods=["POST", "GET"])
def delete():
    form = forms.Delete() # Defining delete form
    if request.method == 'POST' and form.validate():
        item_name = form.item.data.strip()
        backpack_item = Backpack.query.filter_by(item=item_name).first()
        if backpack_item == None:
            print("no such item in db")
        elif backpack_item.amount > 1:
            backpack_item.amount = backpack_item.amount - 1
            db.session.commit()
        else:
            db.session.delete(backpack_item)
            db.session.commit()
    return redirect('/')

@app.route('/increase', methods=["POST", "GET"])
def increase():
    if request.method == 'POST':
        item = request.form.get("item_name")
        database_item = Backpack.query.filter_by(item=item).first()
        database_item.amount = database_item.amount + 1
        db.session.commit()
    return redirect('/')

@app.route('/decrease', methods=["POST", "GET"])
def decrease():
    if request.method == 'POST':
        item = request.form.get("item_name")
        database_item = Backpack.query.filter_by(item=item).first()
        if database_item.amount > 1:
            database_item.amount = database_item.amount - 1
            db.session.commit()
        else:
            db.session.delete(database_item)
            db.session.commit()
    return redirect('/')

@app.errorhandler(404)
def error404(e):
    return render_template("error404.html")

if __name__ == "__main__":
    app.run(debug=True)