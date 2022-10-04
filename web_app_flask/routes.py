from flask import render_template
from web_app_flask import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home Page')

@app.route('/account')
def account():
    return render_template('Account.html', title='Account')

@app.route('/about')
def about():
    return render_template('About.html', title='About Us')

@app.route('/register')
def register():
    return render_template('Register.html', title='Sign Up')

@app.route('/signin')
def signin():
    return render_template('SignIn.html', title='Log In')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404