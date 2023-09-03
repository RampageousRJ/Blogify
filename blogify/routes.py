from flask import Flask,render_template
from blogify import app

@app.route('/')
@app.route('/landing')
def home():
    return "<p>Hello World</p>"