from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .student_forms import StudentForm
from .student_models import (
    get_programs, get_students, add_student, get_student_by_id,
    update_student, delete_student, student_exists
)
from cloudinary.uploader import upload, destroy

student_bp = Blueprint('student', __name__, url_prefix='/student')

def is_image_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'svg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@student_bp.route('/', methods=['GET', 'POST'])
def student_page():
    db = current_app.config['db']
    
    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'ID Number')

    programs = get_programs(db)
    students = get_students(db, search_query, search_by)

    form = StudentForm()
    form.program.choices = [(program[0], program[1]) for program in programs]

    return render_template('student.html', form=form, students=students)

@student_bp.route('/add', methods=['POST'])
def add_student_route():
    form = StudentForm()
    db = current_app.config['db']
    
    programs = get_programs(db)
    form.program.choices = [(program[0], program[1]) for program in programs]

    if form.validate_on_submit():
        id_number = f"{form.id_number_year.data}-{form.id_number_unique.data}"
        if student_exists(db, id_number):
            form.id_number_unique.errors.append("Student with this ID number already exists.")
            return render_template('student.html', form=form, programs=programs)

        image_url = None
        image_file = request.files.get('student_image')
        if image_file and image_file.filename and is_image_file(image_file.filename):
            try:
                upload_result = upload(image_file)
                image_url = upload_result.get('secure_url')
            except Exception as e:
                form.student_image.errors.append(f"Failed to upload image: {e}")
                return render_template('student.html', form=form, programs=programs)

        student_data = (
            id_number, form.first_name.data, form.last_name.data, form.gender.data,
            form.program.data, form.year_level.data, image_url
        )
        add_student(db, student_data)
        return redirect(url_for('student.student_page'))

    return render_template('student.html', form=form, programs=programs)

@student_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_student(id):
    form = StudentForm()
    db = current_app.config['db']

    student_data = get_student_by_id(db, id)
    if not student_data:
        return redirect(url_for('student.student_page'))  # Student not found

    form.id_number_year.data, form.id_number_unique.data = student_data[0].split('-')
    programs = get_programs(db)
    form.program.choices = [(program[0], program[1]) for program in programs]

    if request.method == 'GET':
        form.first_name.data = student_data[1]
        form.last_name.data = student_data[2]
        form.gender.data = student_data[3]
        form.program.data = student_data[4]
        form.year_level.data = student_data[5]

    if form.validate_on_submit():
        image_url = student_data[6]
        image_file = request.files.get('student_image')
        if image_file and image_file.filename and is_image_file(image_file.filename):
            try:
                upload_result = upload(image_file)
                image_url = upload_result.get('secure_url')
            except Exception as e:
                form.student_image.errors.append(f"Failed to upload image: {e}")
                return render_template('student.html', form=form, programs=programs)

        student_update_data = (
            form.first_name.data, form.last_name.data, form.gender.data,
            form.program.data, form.year_level.data, image_url
        )
        update_student(db, student_update_data, id)
        return redirect(url_for('student.student_page'))

    return render_template('student.html', form=form, programs=programs)

@student_bp.route('/delete/<id>', methods=['POST'])
def delete_student_route(id):
    db = current_app.config['db']
    student_data = get_student_by_id(db, id)
    if student_data:
        image_url = student_data[6]
        delete_student(db, id)
        if image_url:
            try:
                public_id = image_url.split('/')[-1].split('.')[0]
                destroy(public_id)
            except Exception as e:
                print(f"Failed to delete image: {e}")

    return redirect(url_for('student.student_page'))
