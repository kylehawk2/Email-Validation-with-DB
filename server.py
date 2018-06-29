from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "keepitsecretkeepitsafe"

mysql = MySQLConnector(app, 'email_validation_with_db')

@app.route('/')
def index():
  return render_template('index.html', title="Email Home")

@app.route('/create', methods=["POST"])
def create():
  errors = False
  if not EMAIL_REGEX.match(request.form['email']):
    errors = True
    flash("Must be a valid email address")
  query = "SELECT * FROM emails WHERE email = :email"
  data = {
    "email": request.form['email']
  }
  emails = mysql.query_db(query, data)
  print emails
  if len(emails) > 0:
    errors = True
    flash("Email address already added")

  if errors:
    return redirect('/')
  else:
    query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
    data = {
      "email": request.form['email']
    }
    mysql.query_db(query, data)

    flash("The email address you entered is a valid email address")
    return redirect('/success')

@app.route('/success')
def success():
  emails_query = "SELECT * FROM emails"
  emails = mysql.query_db(emails_query)
  return render_template('success.html', title="Email Success", emails=emails)

app.run(debug=True)