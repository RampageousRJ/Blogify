from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)

# OLD SQLite3 DB
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

# NEW MySQL DB
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:rampage@localhost/users'
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
ckeditor = CKEditor(app)

from blogify import routes