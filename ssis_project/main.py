from flask import Blueprint, render_template, current_app, request, redirect, url_for

# create a Blueprint for the main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return render_template("base.html")

@main_bp.route('/student', methods=['GET', 'POST'])
def student_form():
    # access the db from app's config
    db = current_app.config['db']
    
    if request.method == 'POST':
        # Create a new cursor for this request
        cursor = db.cursor()

        # Extract data from the form
        id_number = request.form['id_number_year'] + '-' + request.form['id_number_unique']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        program = request.form['program']
        year_level = request.form['year_level']

        try:
            # Prepare the SQL query
            sql = """
                INSERT INTO student (id_number, first_name, last_name, gender, program, year_level)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            # Execute the query
            cursor.execute(sql, (id_number, first_name, last_name, gender, program, year_level))

            # Commit the changes to the database
            db.commit()
        except Exception as e:
            db.rollback()  # Rollback in case of error
            print(f"Error: {e}")
        finally:
            cursor.close()  # Close the cursor

        # Redirect back to avoid form re-submission
        return redirect(url_for('main.student_form'))

    # If it's a GET request, fetch the programs from the 'program' table
    cursor = db.cursor()
    cursor.execute("SELECT code, name FROM program")
    programs = cursor.fetchall()
    cursor.close()

    return render_template('student.html', programs=programs)