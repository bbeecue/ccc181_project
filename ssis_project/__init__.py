# __init__.py
import os
import cloudinary
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from mysql.connector import connect, Error
from settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_SECRET_KEY

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

def create_app():
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = DB_SECRET_KEY
    
    csrf = CSRFProtect(app)
    
    app.config.from_mapping(
        DB_HOST=DB_HOST,
        DB_USER=DB_USER,
        DB_PASSWORD=DB_PASSWORD,
        DB_NAME=DB_NAME,
    )
    
    
    import cloudinary.uploader
    import cloudinary.api
    
    # establish database connection
    try:
        db = connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME'],
        )
        app.config['db'] = db
    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    # Register blueprints
    from .main import main_bp
    app.register_blueprint(main_bp)
    
    from .student.student import student_bp
    app.register_blueprint(student_bp)
    
    from .program.program import program_bp
    app.register_blueprint(program_bp)
    
    from .college.college import college_bp
    app.register_blueprint(college_bp)
    
    

    return app
