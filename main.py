#!/usr/bin/env python3
from flask import Flask, render_template, url_for, redirect, request

import Registration

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register/', methods=['POST', 'GET'])
def registering():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        email = request.args.get('email')
        fullname = request.args.get('name')
        dob = request.args.get('dob')
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fullname = request.form['name']
        dob = request.form['dob']
    if username is None:
        return render_template('register.html')
    else:
        return __database__(username, password, email, dob, fullname)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
    else:
        username = request.form['username']
        password = request.form['password']
    if username is None:
        return render_template('login.html')
    else:
        return __database__(username, password)


def __database__(*args):
    if len(args) == 5:
        username, password, email, dob, name = args
        k = Registration.Dbms(username, password, email, dob, name)
        value = k.registering()
        if value == 0:
            return __database__(username, password)
        elif value == 1:
            return render_template('register.html', email_message="enter valid email", username=username, dob=dob,
                                   name=name)
        elif value == 2:
            return render_template('register.html', email_message="email already registered", username=username,
                                   dob=dob, name=name)
        elif value == 3:
            return render_template('register.html', username_message="username already in use", email=email, dob=dob,
                                   name=name)
        elif value == 4:
            return render_template('register.html', dob_message="enter valid dob", username=username, email=email,
                                   name=name)
        elif value == 5:
            return render_template('register.html', username_message="invalid username", email=email, name=name,
                                   dob=dob)
    else:
        username, password = args
        k = Registration.Dbms(username, password)
        value = k.log_in()
        if value is None:
            return render_template('login.html', message="invalid username or password")
        else:
            return render_template('home.html', username=value[0], email=value[1], dob=value[2], name=value[3])


@app.route('/forget_password/', methods=['POST', 'GET'])
def forget_password():
    if request.method == 'GET':
        email = request.args.get('username')
        dob = request.args.get('dob')
        npassword = request.args.get('password')
        name = request.args.get('name')
    else:
        email = request.form['username']
        dob = request.form['dob']
        npassword = request.form['password']
        name = request.form['name']
    if email is None:
        return render_template('forget.html')
    else:
        k = Registration.Dbms(email, dob, npassword, name)
        value = k.forget()
        if value == 0:
            return render_template('forget.html', message="successful")
        else:
            return render_template('forget.html', message="unsuccessful")


if __name__ == "__main__":
    app.run()
