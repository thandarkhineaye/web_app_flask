from flask import render_template
from web_app_flask import app


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/home')
def home():
    return render_template('home.html')