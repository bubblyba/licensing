import os
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import sqlite3


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class users(db.Model):
    user_id = db.Column("user_id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(50))
    password = db.Column("password", db.String(50))
    email = db.Column("email", db.String(100))




    def __init__(self,username, password, email):


        self.username = username
        self.password = password
        self.email = email


class license(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    document_name = db.Column("document_name", db.String(50))
    issued_by = db.Column("issued_by", db.String(50))
    description = db.Column("description", db.String(50))

    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self,id,document_name,issued_by,user_id):

        self.id = id

        self.document_name = document_name
        self.issued_by = issued_by

        self.user_id = user_id




@app.route('/signup/')
def sign_up_form():
    return render_template('signup.html')


@app.route('/signup/', methods=['POST','GET'])
def signup():
    sqliteConnection = sqlite3.connect('users.sqlite3')

    cursor = sqliteConnection.cursor()


    username = request.form['username']
    password = request.form['password']
    email = request.form['email']



    found_user = users.query.filter_by(username=username).first()
    if found_user:
        error = "That username is taken"
        return render_template('signup.html', error=error)
    else:
        found_email = users.query.filter_by(email=email).first()

        if found_email:
            error = "An account already exists with that email"
            return render_template('signup.html', error=error)
        else:

            usr = users(username, password,email)
            db.session.add(usr)
            db.session.commit()
            role_id = 0
            role_name="viewer"
            sqliteConnection = sqlite3.connect('users.sqlite3')

            cursor = sqliteConnection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username= ?",
                           (username,))
            user_id = cursor.fetchone()
            print(user_id[0])

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


    session['username'] =  username
    cursor.execute("SELECT * FROM users WHERE username= ? and password= ?",
                   (username, password))

    found = cursor.fetchone()
    if found:
        cursor.execute("SELECT user_id FROM users WHERE username= ?",
                       (username,))

        user_id = cursor.fetchone()


        print("good")

        print(user_id)

        return redirect(url_for('dashboard'), username)
    else:
        print("bad")
        error = "Wrong username or password"
        return render_template('login.html', error=error)


@app.route('/dashboard/')
def dashboard_form():
    return render_template('dashboard.html')


@app.route('/dashboard/', methods=['POST'])
def dashboard():

        return render_template('dashboard.html')




if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')


