from flask import Flask,render_template,flash
from blogify import app
from blogify.forms import *

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    favourite_food=['pizza','burger']
    return render_template('user.html',name=name,foods=favourite_food)

@app.route('/name',methods=['GET','POST'])
def name():
    name=None
    form=UserForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=""
        flash("Submitted Successfully!",category='success')
    return render_template('name.html',name=name,form=form)

# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500