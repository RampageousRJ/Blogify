from blogify import app,db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(120),nullable=False,unique=True)
    color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
        return f"<{self.name}>"