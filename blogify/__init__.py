from flask import Flask,render_template

app = Flask(__name__)
app.config['SECRET_KEY']='08731aa961f88a8835c70351'

from blogify import routes