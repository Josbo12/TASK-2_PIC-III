from __future__ import print_function
import sys
import sqlite3
from flask import render_template
from flask import Flask, redirect, url_for, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import User, Base



app = Flask(__name__)

def new_user(username,name,password,email):


    path_to_db = "dadestask2.db"
    engine = create_engine('sqlite:///' + path_to_db)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    new_user = User(username=username,name=name,password=password,email=email)
    session.add(new_user)
    session.commit()


            #conn.execute("insert into users (username,name,password,email) values (?, ?, ?, ?)",
            #         (username,
            #          name,
            #          password,
            #          email))



def get_data():
    conn = sqlite3.connect('dadestask2.db')
    cursor = conn.execute("SELECT username,name,email from users")
    data = [row for row in cursor]
    conn.close()
    return data

def authentication(username, password):
    conn = sqlite3.connect('dadestask2.db')
    cursor = conn.execute("SELECT username, password from users ")
    for row in cursor:
        if row[0] == username:
            if row[1] == password:
                return True
    else:
        return False




@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/insert_user', methods=['GET', 'POST'])
def insert_user():
    if request.method == 'GET':
            return render_template('create_a_new_user.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        if new_user(username,name,password,email):
            return render_template('register_ok.html')
        else:
            return render_template('register_error.html')

@app.route('/register_ok', methods=['GET', 'POST'])
def register_ok():
    return redirect(url_for('hello'))

@app.route('/register_error', methods=['GET', 'POST'])
def register_error():
    return redirect(url_for('insert_user'))




@app.route('/list_of_users', methods=['GET', 'POST'])
def list_of_users():
    list_of_users = get_data()
    return render_template('list_of_users.html',list_of_users=list_of_users)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
            return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if authentication(username, password):
            return render_template('login_ok.html')
        else:
            return render_template('login_error.html')


@app.route('/login_ok', methods=['GET', 'POST'])
def login_ok():
    return redirect(url_for('hello'))

@app.route('/login_error', methods=['GET', 'POST'])
def login_error():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
