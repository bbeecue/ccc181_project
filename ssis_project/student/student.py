# routes and functions
from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .student_forms import StudentForm  

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/', methods=['GET', 'POST'])
def student_page():
    db = current_app.config['db']
    cursor = db.cursor()
    
    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'ID Number')  # Default to 'ID Number'
    
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    
    sql = "SELECT id_number, first_name, last_name, gender, program, year_level FROM student"
    
    if search_query:
        if search_by == "ID Number":
            sql += " WHERE id_number LIKE %s"
        elif search_by == "Name":
            sql += " WHERE CONCAT(first_name, ' ', last_name) LIKE %s"
        elif search_by == "Gender":
            sql += " WHERE LOWER(gender) = LOWER(%s)"
        elif search_by == "Program":
            sql += " WHERE program LIKE %s"
        elif search_by == "Year Level":
            sql += " WHERE year_level LIKE %s"
        
        search_pattern = f"%{search_query}%" if search_by != "Gender" else search_query  # Adjust pattern for Gender
        cursor.execute(sql, (search_pattern,))
    else:
        cursor.execute(sql)

    students = cursor.fetchall()
    
    cursor.close()

    form = StudentForm()
    form.program.choices = [(program[0], program[1]) for program in programs]

    return render_template('student.html', form=form, students=students)

@student_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    db = current_app.config['db']

    # Populate program choices dynamically
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    form.program.choices = [(program[0], program[1]) for program in programs]

    # Fetch students
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
            if existing_student(id_number):
                # If the student ID already exists, show an error message and do not insert the new record
                form.id_number_unique.errors.append("Student with this ID number already exists.")
                return render_template('student.html', form=form, programs=programs, students=students)  # Include students here

            # Insert the new student if ID is unique
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
    current_program_code = student_data[4]
      

    if request.method == 'GET':  
        form.first_name.data = student_data[1]
        form.last_name.data = student_data[2]
        form.gender.data = student_data[3]
        form.program.data = current_program_code
        form.year_level.data = student_data[5]

    if form.validate_on_submit():
        id_number = id 
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        program = form.program.data
        year_level = form.year_level.data

        cursor.execute("""
                UPDATE student SET first_name=%s, last_name=%s, gender=%s, program=%s, year_level=%s WHERE id_number=%s
            """, (first_name, last_name, gender, program, year_level, id_number))
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
        
        cursor.execute("DELETE FROM student WHERE id_number = %s", (id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error deleting student: {e}")
    finally:
        cursor.close()


    return redirect(url_for('student.student_page'))



def existing_student(id_number):
    """Check if a student with the given ID number already exists in the database."""
    db = current_app.config['db']
    cursor = db.cursor()
    
    cursor.execute("SELECT id_number FROM student WHERE id_number = %s", (id_number,))
    student = cursor.fetchone()
    cursor.close()
    
    if student:
        return True  
    return False  
