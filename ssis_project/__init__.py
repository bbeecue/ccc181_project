from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from ssis_project.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


app = Flask(__name__)

#connect to MySQL database
try:
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = db.cursor()
except Error as e:
    print("Error connecting to MySQL", e)

@app.route('/')
def main():
    return render_template("base.html")

@app.route('/test')
def students():
    return render_template("student.html")


if __name__ == '__main__':
    app.run()