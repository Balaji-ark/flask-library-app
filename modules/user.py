from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import User
from . import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['is_admin'] = user.id == 1  # Assuming user ID 1 is the admin
            session.permanent = True  # Make the session permanent
            print("Session after login:", session)  # Debugging: check session after login
            return redirect(url_for('user.library'))  # Redirect to library after successful login
        else:
            return render_template('login.html', error="Invalid credentials")  # Show error message if login fails

    return render_template('login.html')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.login'))  # After registration, redirect to login page

    return render_template('register.html')

@user_bp.route('/up')
def user_profile():
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('user.login'))  # Redirect to login page if not logged in
    return render_template('up.html')  # Return profile page if logged in

@user_bp.route('/library')
def library():
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('user.login'))  # Redirect to login page if not logged in
    return render_template('library.html')  # Return library page if logged in
