from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin

class UserForm(UserMixin,FlaskForm):
    name=StringField("Enter name: ",validators=[DataRequired()])
    email=StringField("Enter email: ",validators=[DataRequired()])
    color=StringField("Enter favourite color: ")
    submit=SubmitField("Submit")
    
class NamerForm(UserMixin,FlaskForm):
    name=StringField("Enter name: ",validators=[DataRequired()])
    submit=SubmitField("Submit")