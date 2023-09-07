from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,ValidationError
from wtforms.validators import DataRequired, EqualTo,Length
from flask_login import UserMixin

class UserForm(UserMixin,FlaskForm):
    name=StringField("Enter name: ",validators=[DataRequired()])
    email=StringField("Enter email: ",validators=[DataRequired()])
    color=StringField("Enter favourite color: ")
    password_hash=PasswordField("Enter password: ",validators=[DataRequired(),EqualTo('password_hash2',message='Passwords must match')])
    password_hash2=PasswordField("Re-type password: ",validators=[DataRequired()])
    submit=SubmitField("Submit")
    
class NamerForm(UserMixin,FlaskForm):
    name=StringField("Enter name: ",validators=[DataRequired()])
    submit=SubmitField("Submit")