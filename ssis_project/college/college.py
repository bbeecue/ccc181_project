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


@college_bp.route('/edit/<code>', methods=['GET', 'POST'])
def edit_college(code):
    form = CollegeForm()
    db = current_app.config['db']
    cursor = db.cursor()
    college_code = code
    
    # Fetch current college details to prepopulate the form
    cursor.execute("SELECT * FROM college WHERE code=%s", (code,))
    college_data = cursor.fetchone()
    
    
    # Fetch colleges
    cursor.execute("SELECT code, name FROM college")
    colleges = cursor.fetchall()
    cursor.close()
    
    
    if request.method == 'GET':  # Only populate on GET requests
        form.college_code.data = college_data[1]
        form.college_name.data = college_data[2]
    
    if form.validate_on_submit():
        new_college_code = form.college_code.data 
        college_name = form.college_name.data
        
        if new_college_code == college_code:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE college SET name=%s WHERE code=%s
            """, (college_name, college_code))
            db.commit()
            cursor.close()
            
        elif existing_college(new_college_code):
            form.college_code.errors.append("College with this code already exists.")
            return render_template('college.html', form=form, colleges=colleges)
        
        else:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE college SET code=%s, name=%s WHERE code=%s
            """, (new_college_code, college_name, college_code))
            db.commit()
            cursor.close()
            
        return redirect(url_for('college.college_page'))
    

    return render_template('college.html', form=form, colleges=colleges)


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
