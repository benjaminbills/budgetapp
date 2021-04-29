from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user, login_required, logout_user
from ..models import User
from . import auth
from .. import db
from .forms import LoginForm,RegistrationForm

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or Password')
    return render_template('auth/login.html', login_form = login_form)

@auth.route('/register',methods = ["GET","POST"])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        user = User(email = register_form.email.data, password = register_form.password.data, username =register_form.username.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', register_form=register_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))