from wtforms import StringField, validators, SubmitField
from flask_wtf import FlaskForm

class Add(FlaskForm):
    item = StringField('Add Item', validators=[validators.length(min=1, max=80), validators.input_required()], render_kw={"placeholder": "Item Name"})

    

class Delete(FlaskForm):
    item = StringField('Delete Item', validators=[validators.length(min=1, max=80), validators.input_required()], render_kw={"placeholder": "Item Name"})

#https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms
#https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/

