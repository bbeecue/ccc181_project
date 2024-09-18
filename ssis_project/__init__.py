# 2022-0380/ssis_project/__init__.py

from flask import Flask
from mysql.connector import connect, Error
from settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from .main import main_bp

def create_app():
    app = Flask(__name__)

    # initialize/establish database connection
    try:
        db = connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        app.config['db'] = db
    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    # register the blueprints
    app.register_blueprint(main_bp)

    return app