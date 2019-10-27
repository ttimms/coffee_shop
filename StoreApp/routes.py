from StoreApp import storeApp, db
from flask import render_template, flash, redirect, url_for, request
from StoreApp.forms import LoginForm, NewProductForm
from StoreApp.models import User, Product
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

@storeApp.route('/')
@storeApp.route('/index')
def index():
  page = request.args.get('page', 1, type=int)
  products = Product.query.filter_by(category='coffee').paginate(page, storeApp.config['PRODUCTS_PER_PAGE'], False)
  next_url = url_for('index', page=products.next_num) if products.has_next else None
  prev_url = url_for('index', page=products.prev_num) if products.has_prev else None
  return render_template('home.html', title='Home', products=products.items, next_url=next_url, prev_url=prev_url)

@storeApp.route('/food')
def food():
  page = request.args.get('page', 1, type=int)
  products = Product.query.filter_by(category='food').paginate(page, storeApp.config['PRODUCTS_PER_PAGE'], False)
  next_url = url_for('food', page=products.next_num) if products.has_next else None
  prev_url = url_for('food', page=products.prev_num) if products.has_prev else None
  return render_template('home.html', title='Home', products=products.items, next_url=next_url, prev_url=prev_url)

@storeApp.route('/treats')
def treat():
  page = request.args.get('page', 1, type=int)
  products = Product.query.filter_by(category='treat').paginate(page, storeApp.config['PRODUCTS_PER_PAGE'], False)
  next_url = url_for('treats', page=products.next_num) if products.has_next else None
  prev_url = url_for('treats', page=products.prev_num) if products.has_prev else None
  return render_template('home.html', title='Home', products=products.items, next_url=next_url, prev_url=prev_url)

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
  page = request.args.get('page', 1, type=int)
  products = Product.query.paginate(page, storeApp.config['PRODUCTS_PER_PAGE'], False)
  next_url = url_for('admin', page=products.next_num) if products.has_next else None
  prev_url = url_for('admin', page=products.prev_num) if products.has_prev else None
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
  return render_template('admin.html', products=products.items, form=form, next_url=next_url, prev_url=prev_url)