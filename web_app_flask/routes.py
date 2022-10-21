from sre_constants import SUCCESS
from flask import render_template, redirect, url_for, flash
from web_app_flask import app ,db
from web_app_flask.forms import RegistrationForm, LogInForm
from web_app_flask.models import User

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

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}', 'success')
        return  redirect(url_for('signin'))
    return render_template('Register.html', title='Sign Up', form=form)

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if form.email.data == user.email and form.password.data == user.password:
            flash(f'Sign In successful for {form.email.data}', category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Sign In unsuccessful for {form.email.data}', category='danger')
    return render_template('SignIn.html', title='Log In', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404