from wtforms import FlaskForm, StringField, validators, SubmitField

class Add(Form):
    item = StringField('Item', [validators.length(max=80)])
    submit = SubmitField('Submit')

    #FlaskForm or Form




