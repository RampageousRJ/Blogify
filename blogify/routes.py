from flask import render_template,flash,request,redirect,url_for
from blogify import app,db,load_dotenv,mail
from blogify.forms import *
from blogify.models import *
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user
from flask_mail import Message
from random import randint
import re
import os
load_dotenv()

def validEmail(email_text):
    if re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email_text) is not None:
        return True
    return False

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form=UserForm()
    if form.validate_on_submit():
        if not validEmail(form.email.data):
            flash("Invalid Email Address!")
            return render_template('register.html',form=form)
        user_exists = Users.query.filter_by(email=form.email.data).first()
        name_repeat = Users.query.filter_by(username=form.username.data).first()
        if name_repeat:
            flash("Username already exists! Try logging in or using a different ID.")
            return render_template('register.html',form=form)
        if user_exists:
            flash("Email already exists! Try logging in or using a different ID.")
            return render_template('register.html',form=form)
        hpw = generate_password_hash(form.password_hash.data,"sha256")
        os.environ['NEW_NAME']=form.name.data
        os.environ['NEW_EMAIL']=form.email.data
        os.environ['NEW_PASS']=hpw
        os.environ['NEW_USERNAME']=form.username.data
        
        os.environ['OTP']=str(randint(100000,999999))
        msg = Message("OTP Verficiation",body=f"Use this OTP to verify your email address for Blogify! \n\n{os.getenv('OTP')}",sender=('Blogify','automailer.0123@gmail.com'),recipients=[form.email.data.strip()])
        # mail.send(msg)
        flash("OTP sent!")
        form.name.data = ""
        form.username.data = ""
        form.email.data = ""
        form.password_hash=""
        return redirect(url_for('otp',user=os.getenv('NEW_USERNAME')))
    if current_user.is_authenticated:
        flash('ERROR: cannot access when logged in!')
        return redirect(url_for('dashboard')) 
    return render_template('register.html',form=form)

@app.route('/otp/<user>',methods=['GET','POST'])
def otp(user):
    print(os.getenv('OTP'))
    form = OTPForm()
    user = Users(name=os.getenv('NEW_NAME'),email=os.getenv('NEW_EMAIL'),password_hash=os.getenv('NEW_PASS'),username=os.getenv('NEW_USERNAME'))
    if request.method=='POST':
        if int(form.otp.data) == int(os.getenv('OTP')):
            db.session.add(user)
            db.session.commit()
            flash("Registered Successfully!")
            return redirect(url_for('login'))
        else:
            flash("OTP Invalid! Try again!")
    return render_template('otp.html',form=form,user=user)

@app.route('/user/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    updated_name = Users.query.get_or_404(id)
    if request.method=='POST':
        updated_name.name = request.form['name']
        updated_name.email = request.form['email']
        updated_name.color = request.form['color']
        updated_name.about = request.form['about']
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
    try:
        db.session.delete(delete_user)
        db.session.commit()
        flash("User Deleted Successfully!")
    except:
        flash("Error! Please try again!")
    return redirect(url_for('login'))

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
    posts = Post.query.order_by(Post.date_added.desc())
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
    id = current_user.id
    if post.blogger.id != id:
        flash("You are not authorized to edit this post! Redirecting to dashboard...")
        return redirect(url_for('dashboard'))
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
    return render_template('edit_post.html',form=form,post=post)

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
    if current_user.is_authenticated:
        flash('ERROR: You are already logged in!')
        return redirect(url_for('dashboard'))             
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
        updated_name.about = request.form['about']
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
    flash("You have successfully logged out!")
    return redirect('home')
    
@app.route('/search',methods=['POST'])
def search():
    posts = Post.query
    form = SearchForm()
    if form.validate_on_submit():
        searched_value = form.searched.data
        posts = posts.filter(Post.title.like("%"+searched_value+"%"))
        posts = posts.order_by(Post.title).all()
        return render_template('search.html',form=form, searched=searched_value,posts=posts)
    return render_template('search.html',form=form, search="NONE")
    
# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500