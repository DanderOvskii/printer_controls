from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
import os

bp = Blueprint('auth', __name__)

username = os.getenv('USERNAME', 'default_user')
password = os.getenv('PASSWORD', 'default_password')
user = User(id=1, username=username, password_hash=generate_password_hash(password))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == user.username and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
