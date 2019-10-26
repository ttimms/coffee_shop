from StoreApp import storeApp
from flask import render_template, flash, redirect, url_for
from StoreApp.forms import LoginForm
from StoreApp.models import User
from flask_login import current_user, login_user, logout_user, login_required

@storeApp.route('/')
@storeApp.route('/index')
def index():
  products = ({"name": "Cappuccino", "price": "5.00", "image": "static/img/cappuccino.png"},
              {"name": "Black Coffee", "price": "2.00", "image": "static/img/coffee.png"},
              {"name": "Iced Coffee", "price": "3.00", "image": "static/img/iced_coffee.jpeg"} 
            )
  return render_template('home.html', title='Home', products=products)

@storeApp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('admin'))
  return render_template('login.html', title='Sign In', form=form)

@storeApp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@storeApp.route('/admin')
@login_required
def admin():
  return 'admin page'