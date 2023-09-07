from blogify import app,db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(120),nullable=False,unique=True)
    color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f"<{self.name}>"