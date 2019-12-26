from StoreApp import storeApp, db
from flask import render_template, flash, redirect, url_for, request
from StoreApp.forms import LoginForm, NewProductForm, ContactForm
from StoreApp.models import User, Product
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from StoreApp.email import send_receipt, send_message, send_sale_notification
import os
import stripe

@storeApp.route('/')
@storeApp.route('/index')
@storeApp.route('/index/<cat>')
def index(cat='coffee'):
  page = request.args.get('page', 1, type=int)
  products = Product.query.filter_by(category=cat).paginate(page, storeApp.config['PRODUCTS_PER_PAGE'], False)
  next_url = url_for('index', page=products.next_num) if products.has_next else None
  prev_url = url_for('index', page=products.prev_num) if products.has_prev else None
  key = storeApp.config['STRIPE_PUBLISHABLE_KEY']
  flash(' DISCLAIMER: Anything purchased on this website is purchased for Tyler Timms. You will receive nothing for your purchase beyond his unspoken gratitude and a thoughtful computer generated thank you email.', 'warning')
  return render_template('home.html', 
                          title='Home', 
                          products=products.items, 
                          next_url=next_url, 
                          prev_url=prev_url, 
                          stripe_public_key=key)

@storeApp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password', 'danger')
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
  products = Product.query.paginate(page, storeApp.config['ADMIN_PRODUCTS_PER_PAGE'], False)
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
    flash('Item: ' + newProduct.name + ' successfully added to store.', 'success')
    return redirect(url_for('admin'))
  return render_template('admin.html', title='Admin', products=products.items, form=form, next_url=next_url, prev_url=prev_url)

@storeApp.route('/delete_product', methods=['GET', 'POST'])
@login_required
def delete_product():
  if current_user.role == 'Admin':
    product_id = request.args.get('pid')
    if product_id:
      product = Product.query.filter_by(id = product_id).first()
      product_name = product.name
      os.remove(storeApp.config['UPLOAD_FOLDER'] + product.image_path)
      db.session.delete(product)
      db.session.commit()
      flash('Item: ' + product_name + ' successfully removed from store.', 'success')
      return redirect(url_for('admin'))
  return redirect(url_for('login'))

@storeApp.route('/process_payment/<id>', methods=['GET', 'POST'])
def process_payment(id):
  product = Product.query.filter_by(id=id).first()
  customer = stripe.Customer.create(
    email = request.form['stripeEmail'],
    source = request.form['stripeToken']
  )
  stripe.Charge.create(
    customer = customer.id,
    amount = int(product.price * 100),
    currency = 'usd',
    description = 'Purchase for ' + product.name
  )
  send_receipt(customer.email, product)
  send_sale_notification(customer.email, product, product.price)
  flash('Purchase made successfully! Thank you very much! A receipt will be sent to the provided email.', 'success')
  return redirect(url_for('index'))

@storeApp.route('/about')
def about():
  return render_template('about.html', title='About')
  
@storeApp.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  if request.method == 'POST':
    Name = form.name.data
    Email = form.email.data
    Message = form.message.data
    flash('Thank you for getting in touch! I\'ll respond to your message as soon as I am able!', 'success')
    send_message(Email, Name, Message)
    return redirect(url_for('index'))
  return render_template('contact.html', title='Contact', form=form)
