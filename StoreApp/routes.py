from StoreApp import storeApp
from flask import render_template

@storeApp.route('/')
@storeApp.route('/index')
def index():
  products = ({"name": "Cappuccino", "price": "5.00", "image": "static/img/cappuccino.png"},
              {"name": "Black Coffee", "price": "2.00", "image": "static/img/coffee.png"},
              {"name": "Iced Coffee", "price": "3.00", "image": "static/img/iced_coffee.jpeg"} 
            )
  return render_template('home.html', title='Home', products=products)