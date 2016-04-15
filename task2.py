from __future__ import print_function
import sys
import sqlite3
from flask import render_template
from flask import Flask, redirect, url_for, request
from datetime import datetime, date

app = Flask(__name__)

def save_data(username,name,password,email):
    conn = sqlite3.connect('dadestask2.db')
    try:
        conn.execute("insert into users (username,name,password,email) values (?, ?, ?, ?)",
                 (username,
                  name,
                  password,
                  email))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def get_data():
    conn = sqlite3.connect('dadestask2.db')
    cursor = conn.execute("SELECT username,name,email from users")
    data = [row for row in cursor]
    conn.close()
    return data

def authentication(self, username, password):
    conn = sqlite3.connect('dadestask2.db')
    cursor = conn.execute("SELECT username,password from users where username")
    for row in cursor:
        if row[0] == username:
            if row[1] == password:
                return True
    else:
        return False


#def get_zones():
#    conn = sqlite3.connect('dadestask2.db')
#    cursor = conn.execute("select distinct zone from temps;")
#    data = [row[0] for row in cursor]
#    conn.close()
#    return data

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/insert_user', methods=['GET', 'POST'])
def insert_user():
    if request.method == 'GET':
            return render_template('create_a_new_user1.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        email = request.form.get('email')
        if save_data(username,name,password,email):
            return redirect(url_for('hello'))
        else:
            return "Error inserting user"

@app.route('/list_of_users', methods=['GET', 'POST'])
def list_of_users():
    list_of_users = get_data()
    return render_template('list_of_users.html',list_of_users=list_of_users)



@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
            return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if authentication(username,password):
            return render_template('login_ok.html',username=username)
        else:
            return "Error Login"
#@app.route('/zone_data', methods=['GET', 'POST'])
#def zone_data():
#    zones = get_zones()
#    if request.method == 'GET':
#        zone_data = []
#    elif request.method == 'POST':
#        zone = request.form.get('area')
#        print(zone, file=sys.stderr)
#        zone_data = get_zone_data(zone)
#    return render_template('zone_data_table.html',zone_data=zone_data, zones=zones)

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
