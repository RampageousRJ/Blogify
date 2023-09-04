from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin

class UserForm(UserMixin,FlaskForm):
    name=StringField("Enter your name: ",validators=[DataRequired()])
    submit=SubmitField("Submit")