import os
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import sqlite3

from sqlalchemy.util import NoneType

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class users(db.Model):
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(50))
    last_name = db.Column("last_name", db.String(50))
    isAuthenticated = db.Column("isAuthenticated", db.Integer)

    def __init__(self, username, password, isAuthenticated):
        self.username = username
        self.password = password
        self.isAuthenticated = isAuthenticated





@app.route('/signup/')
def sign_up_form():
    return render_template('signup.html')


@app.route('/signup/', methods=['POST'])
def signup():

    username = request.form['username']
    password = request.form['password']

    found_user = users.query.filter_by(username=username).first()
    if found_user:
        error = "That username is taken"
        return render_template('signup.html', error=error)
    else:

        isAuthenticated = 0
        usr = users(username, password,isAuthenticated)
        db.session.add(usr)
        db.session.commit()
        print("Record inserted successfully into user table ")
        return redirect(url_for('login'))






@app.route('/login/')
def login_in_form():

        return render_template('login.html')
@app.route('/login/', methods=['POST'])
def login():

    sqliteConnection = sqlite3.connect('users.sqlite3')

    cursor = sqliteConnection.cursor()

    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    cursor.execute("SELECT * FROM users WHERE username= ? and password= ?",
                   (username, password))
    found = cursor.fetchone()
    if found:
        print("good")
        cursor.execute("UPDATE users SET isAuthenticated = '1' WHERE username = ?",
                       (username,))
        return redirect(url_for('dashboard'), username)
    else:
        print("bad")
        error = "Wrong username or password"
        return render_template('login.html', error=error)


@app.route('/dashboard/')


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')


