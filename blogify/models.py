from blogify import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
 
class Users(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    name = db.Column(db.String(30),nullable=False)
    about = db.Column(db.Text(500))
    email = db.Column(db.String(120),nullable=False,unique=True)
    color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    password_hash = db.Column(db.String(128),nullable=False)
    password_hash2 = db.Column(db.String(128))
    posts = db.relationship('Post',backref='blogger',cascade='all,delete')
    comments = db.relationship('Comment',backref='blogger',cascade='all,delete')
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f"<{self.username}>"
    
class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    blogger_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref='post',cascade='all,delete')
    
class Comment(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    blogger_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
class Subscriber(db.Model):
    __tablename__='subscriber'
    id = db.Column(db.Integer,primary_key=True)
    follower = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    following = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)