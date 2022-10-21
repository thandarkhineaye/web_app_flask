from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisfirstflaskapp'
# Configuration for database connection
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webappflask.db'
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)

from web_app_flask import routes
