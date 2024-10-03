# routes and functions
from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .program_forms import ProgramForm  

program_bp = Blueprint('program', __name__, url_prefix='/program')

@program_bp.route('/', methods=['GET', 'POST'])
def program_page():
    db = current_app.config['db']
    cursor = db.cursor()
    
    cursor.execute("SELECT code, name FROM college")
    colleges = cursor.fetchall()
    
    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'Program Code')  

    
    sql = "SELECT code, name, college FROM program"
    
    if search_query:
        if search_by == "Program Code":
            sql += " WHERE code LIKE %s"
        elif search_by == "Program Name":
            sql += " WHERE name LIKE %s"
        elif search_by == "College Code":
            sql += " WHERE college LIKE %s"

        search_pattern = f"%{search_query}%"
        cursor.execute(sql, (search_pattern,))
    else:
        cursor.execute(sql)

    programs = cursor.fetchall()
    
    cursor.close()

    form = ProgramForm()
    form.college_code.choices = [(college[0], college[1]) for college in colleges]
    
    
    
    return render_template('program.html', form=form, programs=programs)



@program_bp.route('/add', methods=['GET', 'POST'])
def add_program():
    form = ProgramForm()
    db = current_app.config['db']
    
    # Populate college choices dynamically
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM college")
    colleges = cursor.fetchall()
    form.college_code.choices = [(college[0], college[1]) for college in colleges]

    # Fetch programs
    cursor.execute("SELECT code, name, college FROM program")
    programs = cursor.fetchall()
    
    if form.validate_on_submit():
        cursor = db.cursor()
        program_code = form.program_code.data
        program_name = form.program_name.data
        college_code = form.college_code.data
        
        try:
            if existing_program(program_code):
                # If the program already exists, show an error message and do not insert the new record
                form.college_code.errors.append("Program with this code already exists.")
                return render_template('program.html', form=form, colleges=colleges, programs=programs)  
            
            # Insert the new program if program code is unique
            sql = """
                INSERT INTO program (code, name, college)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (program_code, program_name, college_code))
            db.commit()

        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            cursor.close()

        return redirect(url_for('program.program_page'))
    
    print(f"Error here: {form.errors}")

    return render_template('program.html', form=form, colleges=colleges, programs=programs)  


@program_bp.route('/edit/<program_code>', methods=['GET', 'POST'])
def edit_program(program_code):
    form = ProgramForm()
    db = current_app.config['db']
    cursor = db.cursor()
    
    # Fetch programs
    cursor.execute("SELECT code, name, college FROM program")
    programs = cursor.fetchall()
    
    # Fetch current program details to prepopulate the form
    cursor.execute("SELECT code, name, college FROM program WHERE code=%s", (program_code,))
    program_data = cursor.fetchone()
    
    # Fetch colleges
    cursor.execute("SELECT code, name FROM college")
    colleges = cursor.fetchall()
    form.college_code.choices = [(college[0], college[1]) for college in colleges]  # Set choices as (college_code, college_name)
    
    cursor.close()
    
    # Prepopulate the form with the program's data
    if request.method == 'GET':
        form.program_code.data = program_data[0]
        form.program_name.data = program_data[1]
        form.college_code.data = program_data[2]  # Set the current college_code to prepopulate the dropdown
    
    if form.validate_on_submit():
        new_program_code = form.program_code.data 
        program_name = form.program_name.data
        college_code = form.college_code.data
        
        cursor = db.cursor()
        cursor.execute("""
            UPDATE program SET code=%s, name=%s, college=%s WHERE code=%s
        """, (new_program_code, program_name, college_code, program_code))
        db.commit()
        cursor.close()
        
        return redirect(url_for('program.program_page'))
    
    return render_template('program.html', form=form, programs=programs, colleges=colleges)



@program_bp.route('/delete/<program_code>', methods=['POST'])
def delete_college(program_code):
    db = current_app.config['db']
    cursor = db.cursor()

    try:
        # Delete the student with the given ID from the database
        cursor.execute("DELETE FROM program WHERE code = %s", (program_code,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error deleting program: {e}")
    finally:
        cursor.close()

    # Redirect back to the student page after deletion
    return redirect(url_for('program.program_page'))


def existing_program(program_code):
    """Check if prgram with the given code already exists in the database."""
    db = current_app.config['db']
    cursor = db.cursor()
    
    cursor.execute("SELECT code FROM program WHERE code = %s", (program_code,))
    program = cursor.fetchone()
    cursor.close()
    
    if program:
        return True  # college already exists
    return False  # No student found
