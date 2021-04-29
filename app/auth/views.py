from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user, login_required, logout_user
from ..models import User
from . import auth
from .. import db
from .forms import LoginForm,RegistrationForm

@auth.route('/login',methods=['GET','POST'])
def login():
    return render_template('auth/login.html', login_form = login_form)

@auth.route('/register',methods = ["GET","POST"])
def register():
    return render_template('auth/register.html', register_form=register_form)

