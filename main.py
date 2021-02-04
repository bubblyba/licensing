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
    valid_from = db.Column("valid_from", db.String(50))
    valid_to = db.Column("valid_to", db.String(50))
    renewal_link = db.Column("renewal_link", db.String(50))
    notify_on = db.Column("notify_on", db.String(50))
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self,document_name,issued_by,description,valid_from,valid_to,renewal_link,notify_on,user_id):


        self.document_name = document_name
        self.issued_by = issued_by
        self.description = description
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.renewal_link = renewal_link
        self.notify_on = notify_on
        self.user_id = user_id


@app.route('/', methods=['POST','GET'])
def home():
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
	    if request.form.get("submit_a"):
		    return redirect(url_for('login'))
	    elif request.form.get("submit_b"):
		    return redirect(url_for('signup'))


@app.route('/signup/')
def sign_up_form():
    return render_template('signup.html')


@app.route('/signup/', methods=['POST','GET'])
def signup():
    sqliteConnection = sqlite3.connect('users.sqlite3')



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
    print(username)
    cursor.execute("SELECT * FROM users WHERE username= ? and password= ?",
                   (username, password))

    found = cursor.fetchone()
    if found:
        cursor.execute("SELECT user_id FROM users WHERE username= ?",
                       (username,))

        user_id = cursor.fetchone()


        print("good")

        print(user_id[0])
        session['user_id'] = user_id[0]

        return redirect(url_for('dashboard'),302)
    else:
        print("bad")
        error = "Wrong username or password"
        return render_template('login.html', error=error)


@app.route('/dashboard/')
def dashboard_form():

    username = session.get('username')
    if username is None:
        error = "User not authenticated"
        return render_template('error.html', error=error)
    user_id = session.get('user_id')
    if user_id is None:
        error = "User not authenticated"
        return render_template('error.html', error=error)
    sqliteConnection = sqlite3.connect('users.sqlite3')

    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM license WHERE user_id= ?",
                   (user_id,))

    found = cursor.fetchall()




    length = len(found)
    print(username)
    return render_template('dashboard.html',username=username, found=found,length=length)


@app.route('/dashboard/', methods=['POST','GET'])
def dashboard():
    username = session.get('username')
    user_id = session.get('user_id')
    print(user_id)
    print(username)
    return redirect(url_for('add_license_form'), 302)


@app.route('/add_license/')
def add_license():
    username = session.get('username')
    user_id = session.get('user_id')

    print(username)
    return render_template('add_license.html',username=username)


@app.route('/add_license/', methods=['POST'])
def add_license_form():
    username = session.get('username')
    if username is None:
        error = "User not authenticated"
        return render_template('error.html', error=error)

    user_id1 = session.get('user_id')
    if user_id1 is None:
        error = "User not authenticated"
        return render_template('error.html', error=error)
    document_name = request.form['document_name']
    if document_name == "":
        error = "Please provide a document name"
        return render_template('add_license.html', error=error)
    issued_by = request.form['issued_by']
    if issued_by == "":
        error = "Please provide the company that this license is issued by"
        return render_template('add_license.html', error=error)
    description = request.form['description']
    if description == "":
        error = "Please provide a description"
        return render_template('add_license.html', error=error)
    valid_from = request.form['valid_from']
    if valid_from == "":
        error = "Please provide the date that you last renewed you license"
        return render_template('add_license.html', error=error)
    valid_to = request.form['valid_to']
    if valid_to == "":
        error = "Please provide the date that your license expired"
        return render_template('add_license.html', error=error)
    renewal_link = request.form['renewal_link']
    if valid_to == "":
        error = "Please provide the url that you need to go for renewing your license"
        return render_template('add_license.html', error=error)
    notify_on = request.form['notify_on']
    if valid_to == "":
        error = "Please provide the day you would like us to notify you"
        return render_template('add_license.html', error=error)
    user_id = user_id1



    sqliteConnection = sqlite3.connect('users.sqlite3')

    cursor = sqliteConnection.cursor()

    licenses = license(document_name,issued_by,description,valid_from,valid_to,renewal_link,notify_on,user_id)
    db.session.add(licenses)
    db.session.commit()

    return redirect(url_for('dashboard'), 302)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')


