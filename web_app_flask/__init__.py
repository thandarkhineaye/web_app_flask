from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisfirstflaskapp'
# Configuration for database connection
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webappflask.db'
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# reference to Gmil SMPT setup setting 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tkatesting@gmail.com'
app.config['MAIL_PASSWORD'] = ''

# instance for mail
mail = Mail(app)


from web_app_flask import routes
