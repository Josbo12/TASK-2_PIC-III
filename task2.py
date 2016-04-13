from __future__ import print_function
import sys
import sqlite3
from flask import render_template
from flask import Flask, redirect, url_for, request
from datetime import datetime, date

app = Flask(__name__)

def save_data(zone,temp):
    conn = sqlite3.connect('mydatabase.db')
    try:
        conn.execute("insert into temps (tdate,ttime,zone,temperature) values (?, ?, ?, ?)",
                 (date.today(),
                  datetime.now().strftime("%H:%M:%S"),
                  zone,
                  temp))
        conn.commit()
        conn.close()
        return True
    except:
        return False


def get_data():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.execute("SELECT tdate,ttime,zone,temperature from temps")
    data = [row for row in cursor]
    conn.close()
    return data

def get_zone_data(zone):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.execute("SELECT tdate,ttime,zone,temperature from temps WHERE zone = ?",(zone,))
    data = [row for row in cursor]
    conn.close()
    return data

def get_zones():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.execute("select distinct zone from temps;")
    data = [row[0] for row in cursor]
    conn.close()
    return data

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/insert_user', methods=['GET', 'POST'])
def insert_user():
    if request.method == 'GET':
            return render_template('create_a_new_user.html')
    elif request.method == 'POST':
        user = request.form.get('user')
        name = request.form.get('name')
        mail = request.form.get('mail')
        password = request.form.get('password')
        if save_data(zone,temp,mail,password):
            return redirect(url_for('hello'))
        else:
            return "Error inserting user"

@app.route('/hist_data', methods=['GET', 'POST'])
def hist_data():
    historical_data = get_data()
    return render_template('historical_data_table.html',historical_data=historical_data)

@app.route('/zone_data', methods=['GET', 'POST'])
def zone_data():
    zones = get_zones()
    if request.method == 'GET':
        zone_data = []
    elif request.method == 'POST':
        zone = request.form.get('area')
        print(zone, file=sys.stderr)
        zone_data = get_zone_data(zone)
    return render_template('zone_data_table.html',zone_data=zone_data, zones=zones)

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
