from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

storeApp = Flask(__name__)
storeApp.config.from_object(Config)
db = SQLAlchemy(storeApp)
migrate = Migrate(storeApp, db)

from StoreApp import routes, models