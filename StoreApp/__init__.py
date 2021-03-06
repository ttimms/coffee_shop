from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import stripe

storeApp = Flask(__name__)
storeApp.config.from_object(Config)
db = SQLAlchemy(storeApp)
migrate = Migrate(storeApp, db)
login = LoginManager(storeApp)
login.login_view = 'login'
mail = Mail(storeApp)
stripe.api_key = storeApp.config['STRIPE_SECRET_KEY']

from StoreApp import routes, models, errors