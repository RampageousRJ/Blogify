from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,ValidationError
from wtforms.validators import DataRequired, EqualTo,Length
from wtforms.widgets import TextArea
from flask_login import UserMixin

class UserForm(UserMixin,FlaskForm):
    name=StringField("Enter name: ",validators=[DataRequired()])
    username=StringField("Enter username: ",validators=[DataRequired()])
    email=StringField("Enter email: ",validators=[DataRequired()])
    color=StringField("Enter favourite color: ")
    password_hash=PasswordField("Enter password: ",validators=[DataRequired(),EqualTo('password_hash2',message='Passwords must match'),Length(8)])
    password_hash2=PasswordField("Re-type password: ",validators=[DataRequired()])
    submit=SubmitField("Submit")
    
class NamerForm(UserMixin,FlaskForm):
    name=StringField("Enter name: ",validators=[DataRequired()])
    submit=SubmitField("Submit")
    
class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = StringField("Content",validators=[DataRequired()],widget=TextArea())
    slug = StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Confirm")
    
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField('Submit')