from flask import Blueprint, render_template, request, flash, redirect, url_for
# this file is gonna be a blueprint for our app : it will have a lots of routes inside of it
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login',  methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user :
            if check_password_hash(user.password, password):
                flash('logged in successfully !', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else :
                flash('incorrect password ! try again.', category='error')
        else :
            flash('email do not exist', category='error')
        
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST' :
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user : 
            flash('email already exists !', category='error')
        elif len(email) < 5 :
            flash('Email must be greater than 5 characters' , category='error')
        elif len(firstname) <2:
            flash('Firstname must be greater than 2 characters', category='error')
        elif password1 !=password2 :
            flash('passwords don\'t match', category='error')
        elif len(password1) < 7 : 
            flash('password is too short' , category='error')
        else :
            new_user = User(email = email, firstname=firstname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created successfully !' , category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user= current_user)