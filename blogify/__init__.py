from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
from flask_mail import Mail
from flask_moment import Moment
import os
load_dotenv()
app = Flask(__name__)

# OLD SQLite3 DB
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

# NEW MySQL DB
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URI")
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('BLOGIFY_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('BLOGIFY_PRIVATE_KEY')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_ID')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
ckeditor = CKEditor(app)
mail = Mail(app)

from blogify import routes