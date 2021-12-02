from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(Email=email).first()
        if user:
            if check_password_hash(user.Password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid password', category='error')
        else:
            flash('Email does not exist', category='error')
            
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')
        rePassword = request.form.get('rePassword')
        
        user = User.query.filter_by(Email=email).first()
        if user:
            flash('Email is already in use', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif password != rePassword:
            flash('Password don\'t match', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(Email=email, FirstName=firstName, LastName=lastName, Password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account success created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)

