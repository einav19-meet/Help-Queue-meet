from flask import Flask, render_template,send_from_directory, redirect, request, url_for, session as login_session
import os
import datetime
from database import *

#app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf movies'

@app.route('/', methods = ['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_password(username, password):
            login_session['username'] = username
            return redirect(url_for('home'))
        else:
            msg = "login failed: username and password does not match"
    return render_template('login.html', msg = msg)

@app.route('/home', methods = ['GET', 'POST'])
def home():
    if 'username' in login_session:
        username = login_session['username']
        staff = False
        if get_user(username).role != 'student':
            staff = True
        if request.method == 'POST':
            question = request.form['question']
            add_request(username, question)


        amount = len(get_reqs())

        return render_template('index2.html',username = username, reqs = get_student_reqs(username), amount = amount, staff = staff)
    else:
        return redirect(url_for('login'))

@app.route('/view', methods = ['GET', 'POST'])
def view():
    if 'username' in login_session:
        username = login_session['username']
        if get_user(username).role != 'student':
            reqs = get_reqs()
            amount = len(reqs)
            if request.method == 'POST':
                ID = request.form['ID']
                update(ID,username)
                print(get_reqs())
                return redirect(url_for('view'))
            return render_template('view.html', username = username, amount = amount, reqs = reqs, requests = get_user(username).counter)
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)