from StoreApp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from StoreApp import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64))

    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
      return '<User: {}>'.format(self.username)
    
    @login.user_loader
    def load_user(id):
      return User.query.get(int(id))

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String(64))
  name = db.Column(db.String(64))
  price = db.Column(db.Float)
  description = db.Column(db.String(128))
  image_path = db.Column(db.String(128))
