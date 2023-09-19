from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextAreaField
from wtforms.validators import DataRequired, EqualTo,Length
from wtforms.widgets import TextArea
from flask_login import UserMixin
from flask_ckeditor import CKEditorField

class UserForm(UserMixin,FlaskForm):
    name=StringField("Enter name: ",validators=[DataRequired()])
    username=StringField("Enter username: ",validators=[DataRequired()])
    about=TextAreaField("Enter about section: ")
    email=StringField("Enter email: ",validators=[DataRequired()])
    color=StringField("Enter favourite color: ")
    password_hash=PasswordField("Enter password: ",validators=[DataRequired(),EqualTo('password_hash2',message='Passwords must match'),Length(8)])
    password_hash2=PasswordField("Re-type password: ",validators=[DataRequired()])
    submit=SubmitField("Submit")
    
class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = CKEditorField("Content",validators=[DataRequired()])
    slug = StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Confirm")
    
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class SearchForm(FlaskForm):
    searched = StringField("Searched",validators=[DataRequired()])
    submit = SubmitField("Submit")