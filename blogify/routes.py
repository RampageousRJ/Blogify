from flask import Flask,render_template,flash,request,redirect,url_for
from blogify import app,db
from blogify.forms import *
from blogify.models import Users

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
    form=NamerForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=""
        flash("Submitted Successfully!",category='success')
    return render_template('name.html',name=name,form=form)

@app.route('/user/add',methods=['GET','POST'])
def add_user():
    form=UserForm()
    name=None
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            u1 = Users(name=form.name.data,email=form.email.data,color=form.color.data)
            db.session.add(u1)
            db.session.commit()
        form.name.data = ""
        form.email.data = ""
        form.color.data = ""
        flash("Registered Successfully!",category='success')
    curr_users =Users.query.order_by(Users.date_added)
    return render_template('add_user.html',form=form,curr_users=curr_users)

@app.route('/user/update/<int:id>',methods=['GET','POST'])
def update(id):
    form = UserForm()
    updated_name = Users.query.get_or_404(id)
    if request.method=='POST':
        updated_name.name = request.form['name']
        updated_name.email = request.form['email']
        updated_name.color = request.form['color']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return redirect(url_for('add_user'))
        except:
            flash('ERROR! Something went wrong...')
            return redirect(url_for('add_user'))
    return render_template("update.html",form=form,updated_name=updated_name)

@app.route('/delete/<int:id>')
def delete(id):
    delete_user = Users.query.get_or_404(id)
    curr_users =Users.query.order_by(Users.date_added)
    form = UserForm()
    try:
        db.session.delete(delete_user)
        db.session.commit()
        flash("User Deleted Successfully!")
    except:
        flash("Error! Please try again!")
    return redirect(url_for('add_user'))

# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500