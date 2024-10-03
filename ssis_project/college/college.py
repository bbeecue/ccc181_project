# routes and functions
from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .college_forms import CollegeForm  

college_bp = Blueprint('college', __name__, url_prefix='/college')

@college_bp.route('/', methods=['GET', 'POST'])
def college_page():
    db = current_app.config['db']
    cursor = db.cursor()
    
    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'College Code')  # Default to 'ID Number'

    
    sql = "SELECT code, name FROM college"
    
    if search_query:
        if search_by == "College Code":
            sql += " WHERE code LIKE %s"
        elif search_by == "College Name":
            sql += " WHERE name LIKE %s"

        
        search_pattern = f"%{search_query}%"
        cursor.execute(sql, (search_pattern,))
    else:
        cursor.execute(sql)

    colleges = cursor.fetchall()
    
    cursor.close()

    form = CollegeForm()
    
    return render_template('college.html', form=form, colleges=colleges)


"""
@student_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    db = current_app.config['db']

    # Populate program choices dynamically
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    form.program.choices = [(program[0], program[1]) for program in programs]

    # Fetch students to display in the table
    cursor.execute("SELECT id_number, first_name, last_name, gender, program, year_level FROM student")
    students = cursor.fetchall()

    if form.validate_on_submit():
        cursor = db.cursor()
        id_number = f"{form.id_number_year.data}-{form.id_number_unique.data}"
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        program = form.program.data
        year_level = form.year_level.data

        try:
            # Check if the student ID already exists
            cursor.execute("SELECT id_number FROM student WHERE id_number = %s", (id_number,))
            existing_student = cursor.fetchone()

            if existing_student:
                # If the student ID already exists, show an error message and do not insert the new record
                form.id_number_unique.errors.append("Student with this ID number already exists.")
                return render_template('student.html', form=form, programs=programs, students=students)  # Include students here

            # Insert the new student if ID is unique
            sql = " ""
                INSERT INTO student (id_number, first_name, last_name, gender, program, year_level)
                VALUES (%s, %s, %s, %s, %s, %s)
            " ""
            cursor.execute(sql, (id_number, first_name, last_name, gender, program, year_level))
            db.commit()

        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            cursor.close()

        return redirect(url_for('student.student_page'))

    return render_template('student.html', form=form, programs=programs, students=students)  # Ensure students are included here



@student_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_student(id):
    form = StudentForm()
    db = current_app.config['db']
    cursor = db.cursor()
    
    # Fetch current student details to prepopulate the form
    cursor.execute("SELECT * FROM student WHERE id_number=%s", (id,))
    student_data = cursor.fetchone()
    form.id_number_year.data, form.id_number_unique.data = student_data[0].split('-')
    cursor.close()
    
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    form.program.choices = [(program[0], program[1]) for program in programs]
    
    if request.method == 'GET':  # Only populate on GET requests
        form.first_name.data = student_data[1]
        form.last_name.data = student_data[2]
        form.gender.data = student_data[3]
        form.program.data = student_data[4]
        form.year_level.data = student_data[5]


    if form.validate_on_submit():
        id_number = id 
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        program = form.program.data
        year_level = form.year_level.data
        
        
        cursor.execute(" ""
                UPDATE student SET first_name=%s, last_name=%s, gender=%s, program=%s, year_level=%s WHERE id_number=%s
            " "", (first_name, last_name, gender, program, year_level, id_number))
        db.commit()
        cursor.close()
            
        return redirect(url_for('student.student_page'))
    
    print(form.errors)

    return render_template('student.html', form=form, programs=programs)


@student_bp.route('/delete/<id>', methods=['POST'])
def delete_student(id):
    db = current_app.config['db']
    cursor = db.cursor()

    try:
        # Delete the student with the given ID from the database
        cursor.execute("DELETE FROM student WHERE id_number = %s", (id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error deleting student: {e}")
    finally:
        cursor.close()

    # Redirect back to the student page after deletion
    return redirect(url_for('student.student_page'))



def existing_student(id_number):
    " ""Check if a student with the given ID number already exists in the database." ""
    db = current_app.config['db']
    cursor = db.cursor()
    
    cursor.execute("SELECT id_number FROM student WHERE id_number = %s", (id_number,))
    student = cursor.fetchone()
    cursor.close()
    
    if student:
        return True  # Student already exists
    return False  # No student found
"""