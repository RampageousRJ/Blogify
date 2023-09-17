from flask import Flask,render_template,flash,request,redirect,url_for
from blogify import app,db
from blogify.forms import *
from blogify.models import *
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,LoginManager,login_required,logout_user,current_user

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

@app.route('/user/register',methods=['GET','POST'])
def register():
    form=UserForm()
    name=None
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hpw = generate_password_hash(form.password_hash.data,"sha256")
            u1 = Users(name=form.name.data,email=form.email.data,password_hash=hpw,username=form.username.data)
            db.session.add(u1)
            db.session.commit()
        form.name.data = ""
        form.username.data = ""
        form.email.data = ""
        form.password_hash=""
        flash("Registered Successfully!",category='success')
        return redirect(url_for('login'))
    curr_users =Users.query.order_by(Users.date_added)
    return render_template('register.html',form=form,curr_users=curr_users)

@app.route('/user/update/<int:id>',methods=['GET','POST'])
@login_required
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
            return redirect(url_for('dashboard'))
        except:
            flash('ERROR! Something went wrong...')
            return redirect(url_for('dashboard'))
    if current_user.id != id:
        flash("You are not authorized to access this page! Redirecting to dashboard...")
        return redirect(url_for('dashboard'))
    return render_template("update.html",form=form,updated_name=updated_name,id=id)

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
    return redirect(url_for('register'))

@app.route('/add-post',methods=['GET','POST'])
@login_required
def add_post():
    id = current_user.id
    form  = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,blogger_id=id,slug=form.slug.data)
        db.session.add(post)
        db.session.commit()
        flash("Blog Post added successfully!")
        return redirect(url_for('posts'))
    return render_template('add_post.html',form=form)

@app.route('/posts')
def posts():
    posts = Post.query.order_by(Post.date_added)
    return render_template("posts.html",posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    if current_user.is_authenticated:
        id = current_user.id
    else:
        id = -999       
    return render_template('post.html',post=post,id=id)

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post updated successfully!")
        return redirect(url_for('post',id=post.id))
    form.title.data = post.title
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html',form=form)

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    id = current_user.id
    if post.blogger.id != id:
        flash("You are not authorized to delete this post! Redirecting to dashboard...")
        return redirect(url_for('dashboard'))
    try:
        db.session.delete(post)
        db.session.commit()
        flash("Blog post deleted successfully!")
        posts = Post.query.order_by(Post.date_added)
        return render_template("posts.html",posts=posts)
    except:
        flash("Error! Blog post could not be deleted!")
        posts = Post.query.order_by(Post.date_added)
        return render_template("posts.html",posts=posts)
    
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Logged in successfully!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password! Please try a different password!")
        else:
            flash("Username does not exist!")               
    return render_template('login.html',form=form)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id=current_user.id
    updated_name = Users.query.get_or_404(id)
    if request.method=='POST':
        updated_name.name = request.form['name']
        updated_name.username = request.form['username']
        updated_name.email = request.form['email']
        updated_name.color = request.form['color']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return redirect(url_for('dashboard'))
        except:
            flash('ERROR! Something went wrong...')
            return redirect(url_for('dashboard'))
    return render_template('dashboard.html',form=form)

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("Ypu have successfully logged out!")
    return redirect('home')
    
# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500