# Name : Devops_Command_Center
# Version : Alpha
# Author : GE-P
# INFO : This is the authentication code fully connected with postgres + session for more security.
# -------------------------------------------------------------------------------------------------- #


import psycopg2
import psycopg2.extras
import re
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# This is the blueprint who permits sliding project in many files
auth = Blueprint('auth', __name__)

# Load environment variables
load_dotenv()


# The function to connect with the DB.
def get_db_connection():
    conn = psycopg2.connect(host=os.getenv('HOST'),
                            database=os.getenv('DB'),
                            user=os.getenv('USER'),
                            password=os.getenv('PSW'))
    return conn


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Connect with the DB
    conn = get_db_connection()
    # Open a cursor to use query's
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # print(password)

        # Check if account exists using SELECT
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result != fetchall that fetch all the table
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            # print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to index page
                return redirect(url_for('index'))
            else:
                # Account doesn't exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesn't exist or username/password incorrect
            flash('Incorrect username/password')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Connect with the DB
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        _hashed_password = generate_password_hash(password)

        # Check if account exists using SELECT
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # print(account)

        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesn't exist and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)",
                           (fullname, username, _hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty then no POST data
        flash('Please fill out the form!')
    # Show registration again
    return render_template('register.html')


@auth.route('/logout')
def logout():
    # Remove session data this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('auth.login'))
