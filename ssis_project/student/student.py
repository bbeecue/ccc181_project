# student.py
from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .student_forms import AddStudentForm  

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/')
def student_page():
    db = current_app.config['db']
    
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    
    cursor.execute("SELECT id_number, first_name, last_name, gender, program, year_level FROM student")
    students = cursor.fetchall()
    
    cursor.close()

    form = AddStudentForm()
    form.program.choices = [(program[0], program[1]) for program in programs]

    return render_template('student.html', form=form, students=students)

@student_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    db = current_app.config['db']
    
    # Populate program choices dynamically
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    form.program.choices = [(program[0], program[1]) for program in programs]

    if form.validate_on_submit():
        cursor = db.cursor()
        id_number = f"{form.id_number_year.data}-{form.id_number_unique.data}"
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        program = form.program.data
        year_level = form.year_level.data

        try:
            sql = """
                INSERT INTO student (id_number, first_name, last_name, gender, program, year_level)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (id_number, first_name, last_name, gender, program, year_level))
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            cursor.close()

        return redirect(url_for('student.student_page'))

    return render_template('student.html', form=form, programs=programs)


