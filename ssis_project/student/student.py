# routes and functions
import cloudinary
from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .student_forms import StudentForm  
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/', methods=['GET', 'POST'])
def student_page():
    db = current_app.config['db']
    cursor = db.cursor()
    
    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'ID Number')  # Default to 'ID Number'
    
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    
    sql = "SELECT id_number, first_name, last_name, gender, program, year_level, image_url FROM student"
    
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
    cursor.execute("SELECT id_number, first_name, last_name, gender, program, year_level, image_url FROM student")
    students = cursor.fetchall()
    
    

    if form.validate_on_submit():
        cursor = db.cursor()
        image_file = request.files.get('student_image')  # Use request.files
        image_url = None

        if image_file and image_file.filename != '':
            try:
                # Upload image to Cloudinary
                upload_result = upload(image_file)
                image_url = upload_result.get('secure_url')
            except Exception as e:
                form.student_image.errors.append(f"Failed to upload image: {e}")
                print(f"Upload error: {e}")
        else:
            print("No file uploaded or file name is empty.")
        
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
                INSERT INTO student (id_number, first_name, last_name, gender, program, year_level, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (id_number, first_name, last_name, gender, program, year_level, image_url))
            db.commit()

        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            cursor.close()
        
        

        return redirect(url_for('student.student_page'))

    print(form.errors)

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
    student_image_url = student_data[6]
      

    if request.method == 'GET':  
        form.first_name.data = student_data[1]
        form.last_name.data = student_data[2]
        form.gender.data = student_data[3]
        form.program.data = current_program_code
        form.year_level.data = student_data[5]
        
        

    if form.validate_on_submit():
        image_file = request.files.get('student_image')
        delete_image_flag = request.form.get('delete_image') == 'delete'
        image_url = student_image_url  # Default to current image

        # Delete current image if requested
        if delete_image_flag:
            if student_image_url:
                public_id = student_image_url.split('/')[-1].split('.')[0]  # Extract public ID from URL
                destroy(public_id)  # Delete image from Cloudinary
            image_url = None

        # Update with new image if provided and delete old image
        elif image_file and image_file.filename:
            try:
                upload_result = upload(image_file)
                image_url = upload_result.get('secure_url')
                if student_image_url:
                    public_id = student_image_url.split('/')[-1].split('.')[0]
                    destroy(public_id)
            except Exception as e:
                form.student_image.errors.append(f"Failed to upload image: {e}")
                print(f"Upload error: {e}")

        # Update database with new details and image URL
        cursor = db.cursor()
        cursor.execute("""
            UPDATE student SET first_name=%s, last_name=%s, gender=%s, program=%s, year_level=%s, image_url=%s 
            WHERE id_number=%s
        """, (form.first_name.data, form.last_name.data, form.gender.data, form.program.data, form.year_level.data, image_url, id))
        db.commit()
        cursor.close()

        return redirect(url_for('student.student_page'))

    print(form.errors)

    return render_template('student.html', form=form, programs=programs)



@student_bp.route('/delete/<id>', methods=['POST'])
def delete_student(id):
    db = current_app.config['db']
    cursor = db.cursor()
    cursor.execute("SELECT * FROM student WHERE id_number=%s", (id,))
    student_data = cursor.fetchone()
    student_image_url = student_data[6]

    try:
        cursor.execute("DELETE FROM student WHERE id_number = %s", (id,))
        db.commit()
        
        if student_image_url:
                public_id = student_image_url.split('/')[-1].split('.')[0]  # Extract public ID from URL
                destroy(public_id)
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

