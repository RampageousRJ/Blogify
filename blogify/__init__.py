from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False  
app.config['SECRET_KEY']='08731aa961f88a8835c70351'
db = SQLAlchemy(app)

from blogify import routes