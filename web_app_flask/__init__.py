from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisfirstflaskapp'
from web_app_flask import routes

