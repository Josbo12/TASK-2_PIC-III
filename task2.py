from __future__ import print_function
import sys
import sqlite3
from flask import render_template
from flask import Flask, redirect, url_for, request
from datetime import datetime, date

app = Flask(__name__)

def save_data(username,name,password,email):
    conn = sqlite3.connect('dadestask2.db')
    cursor = conn.execute("SELECT username, email from users where username=? and email=?" ,(username,email) )
    #cursor = conn.execute("SELECT username, email from users where (username,email) values (?,?)",username, email )
    #t = [e for e in cursor]
    t=cursor.fetchone()

    if t == None:
            conn.execute("insert into users (username,name,password,email) values (?, ?, ?, ?)",
                     (username,
                      name,
                      password,
                      email))
            conn.commit()
            conn.close()
            return True
    else:
            return False


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
        if save_data(username,name,password,email):
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
