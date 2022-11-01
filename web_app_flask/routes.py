from turtle import reset, title
from flask import render_template, redirect, url_for, flash, request
from web_app_flask import app ,db, bcrypt, mail
from web_app_flask.forms import AccountUpdateForm, RegistrationForm, LogInForm, ResetRequestForm, ResetPasswordForm, AccountUpdateForm
from web_app_flask.models import User, UserDetails
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import os

@app.route('/')
@app.route('/home')
def home(): 
    return render_template('home.html', title='Home Page')

def save_image(picture_file):
    picture_name= picture_file.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_name)
    picture_file.save(picture_path)
    return picture_name


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_image(form.picture.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        user_details = UserDetails(firstname = form.firstname.data,
                                    lastname = form.lastname.data,
                                    user_id= current_user.id)
        db.session.add(user_details)
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data =current_user.details[-1].firstname
        form.lastname.data = current_user.details[-1].lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_url = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('Account.html', title='Account', legend='Account Details', form = form, image_url=image_url)

@app.route('/about')
def about():
    return render_template('About.html', title='About Us')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        bcrypt_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = bcrypt_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}', 'success')
        return  redirect(url_for('signin'))
    return render_template('Register.html', title='Sign Up', form=form)

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Sign In successful for {form.email.data}', category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Sign In unsuccessful for {form.email.data}', category='danger')
    return render_template('SignIn.html', title='Log In', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('signin'))

def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@web_app_flask')
    msg.body = f''' To reset your password. Please follow the link below
    
    {url_for('reset_token', token = token, _external = True)}
    If you didn't send a password reset request. Please ignore this message.
    
    '''

@app.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            flash('Reset Request sent, Check your mail', 'success')
            return redirect(url_for('signin'))
    return render_template('reset_request.html', title='Reset Request', form=form, legend='Reset Password')

@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash('That is invalid token or expired. Please try again.', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password changed! Please login!', 'success')
        return redirect(url_for('signin'))
    return render_template('change_password.html', title="Change Password", legend="Change Password", form=form)