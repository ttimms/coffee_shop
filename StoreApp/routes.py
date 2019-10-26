from StoreApp import storeApp, db
from flask import render_template, flash, redirect, url_for, request
from StoreApp.forms import LoginForm, NewProductForm
from StoreApp.models import User, Product
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

@storeApp.route('/')
@storeApp.route('/index')
def index():
  products = Product.query.all()
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

@storeApp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
  products = Product.query.all()
  form = NewProductForm()
  if form.validate_on_submit():
    file = form.image.data
    if file:
      file.save(storeApp.config['UPLOAD_FOLDER'] + secure_filename(file.filename))
    newProduct = Product(
      category = form.category.data,
      name = form.name.data,
      price = form.price.data,
      description = form.description.data,
      image_path = secure_filename(file.filename)
    )
    db.session.add(newProduct)
    db.session.commit()
    return redirect(url_for('admin'))
  return render_template('admin.html', products=products, form=form)