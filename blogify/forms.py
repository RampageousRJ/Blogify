from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,SubmitField,PasswordField,TextAreaField,IntegerField,EmailField
from wtforms.validators import DataRequired, EqualTo,Length
from flask_login import UserMixin
from flask_ckeditor import CKEditorField

class UserForm(UserMixin,FlaskForm):
    name=StringField("Enter name: ",validators=[DataRequired()])
    username=StringField("Enter username: ",validators=[DataRequired()])
    about=TextAreaField("Enter about section: ")
    email=EmailField("Enter email: ",validators=[DataRequired()])
    color=StringField("Enter favourite color: ")
    password_hash=PasswordField("Enter password: ",validators=[DataRequired(),EqualTo('password_hash2',message='Passwords must match'),Length(8)])
    password_hash2=PasswordField("Re-type password: ",validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit=SubmitField("Submit")
    
class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = CKEditorField("Content",validators=[DataRequired()])
    submit = SubmitField("Confirm")
    
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
    
class SearchForm(FlaskForm):
    searched = StringField("Searched",validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class OTPForm(FlaskForm):
    otp = IntegerField("Enter OTP: ",validators=[DataRequired()])
    submit = SubmitField("Validate")
    
class FeedbackForm(FlaskForm):
    title = StringField("Enter title",validators=[DataRequired()])
    body = TextAreaField("Enter body",validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Submit")