from StoreApp import storeApp
from flask import render_template

@storeApp.route('/')
@storeApp.route('/index')
def index():
  return render_template('home.html', title='Home')