from flask import Flask, request, redirect, render_template, session, flash
import re
from mysqlconnection import MySQLConnector
app = Flask(__name__)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

mysql = MySQLConnector(app, 'email_validation_with_db')
app.secret_key = "ThisIsSecret!"


print("***************** Emails *******************")
print mysql.query_db("select * from emails")


@app.route('/')
def index():
    query = "select * from emails"
    emails = mysql.query_db(query)
    print emails
    return render_template('index.html', all_emails=emails)

@app.route('/emails', methods=['POST'])
def create():
    query = "insert into emails (email, created_at, updated_at) values (:email, now(), now())"
    data = {
        'email': request.form['email']
    }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/success', methods=['POST'])
def success():
    query = "select * from emails where email = :email"
    query2 = "select * from emails"
    email =  request.form['email']
    data = {
             'email': request.form['email']
           }
    value = mysql.query_db(query, data)

    if len(value)==0:
        valid = False
        flash('the email you entered was invalid')
        return redirect('/')
    else: valid = True
    value = mysql.query_db(query2, data)

    return render_template('index.html', valid=valid, all_emails=value, email = email)

app.run(debug=True)