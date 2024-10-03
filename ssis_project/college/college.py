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



@college_bp.route('/add', methods=['GET', 'POST'])
def add_college():
    form = CollegeForm()
    db = current_app.config['db']
    cursor = db.cursor()
    
    # Fetch colleges
    cursor.execute("SELECT code, name FROM college")
    colleges = cursor.fetchall()
    if form.validate_on_submit():
        cursor = db.cursor()
        code = form.college_code.data
        name = form.college_name.data
        
        try:
            if existing_college(code):
                # If the student ID already exists, show an error message and do not insert the new record
                form.college_code.errors.append("College with this code already exists.")
                return render_template('college.html', form=form, colleges=colleges)  
            
            # Insert the new college if code is unique
            sql = """
                INSERT INTO college (code, name)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (code, name))
            db.commit()

        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            cursor.close()

        return redirect(url_for('college.college_page'))
    
    print(form.errors)

    return render_template('college.html', form=form, colleges=colleges)  


"""
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
"""

@college_bp.route('/delete/<code>', methods=['POST'])
def delete_college(code):
    db = current_app.config['db']
    cursor = db.cursor()

    try:
        # Delete the student with the given ID from the database
        cursor.execute("DELETE FROM college WHERE code = %s", (code,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error deleting college: {e}")
    finally:
        cursor.close()

    # Redirect back to the student page after deletion
    return redirect(url_for('college.college_page'))



def existing_college(code):
    """Check if college with the given code already exists in the database."""
    db = current_app.config['db']
    cursor = db.cursor()
    
    cursor.execute("SELECT code FROM college WHERE code = %s", (code,))
    college = cursor.fetchone()
    cursor.close()
    
    if college:
        return True  # college already exists
    return False  # No student found
