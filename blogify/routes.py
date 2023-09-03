from flask import Flask,render_template
from blogify import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    favourite_food=['pizza','burger']
    return render_template('user.html',name=name,foods=favourite_food)

# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500