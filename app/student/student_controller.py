from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .student_forms import StudentForm
from .student_models import StudentModel
from app.program.program_models import ProgramModel
from cloudinary.uploader import upload, destroy

student_bp = Blueprint('student', __name__, url_prefix='/student')

def is_image_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'svg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@student_bp.route('/', methods=['GET', 'POST'])
def student_page():
    db = current_app.config['db']
    student_model = StudentModel(db)
    program_model = ProgramModel(db)

    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'ID Number')

    programs = program_model.get_programs()
    students = student_model.get_students(search_query, search_by)

    form = StudentForm()
    form.program.choices = [(None, 'None')] + [(program[0], program[1]) for program in programs]

    return render_template('student.html', form=form, students=students)

@student_bp.route('/add', methods=['POST'])
def add_student_route():
    form = StudentForm()
    db = current_app.config['db']
    student_model = StudentModel(db)
    program_model = ProgramModel(db)

    programs = program_model.get_programs()
    form.program.choices = [(None, 'None')] + [(program[0], program[1]) for program in programs]

    if form.validate_on_submit():
        id_number = f"{form.id_number_year.data}-{form.id_number_unique.data}"
        if student_model.student_exists(id_number):
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

        student_data = {
            "id_number": id_number,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "gender": form.gender.data,
            "program": form.program.data,
            "year_level": form.year_level.data,
            "image_url": image_url
        }
        student_model.add_student(student_data)
        return redirect(url_for('student.student_page'))

    return render_template('student.html', form=form, programs=programs)

@student_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_student(id):
    form = StudentForm()
    db = current_app.config['db']
    student_model = StudentModel(db)
    program_model = ProgramModel(db)

    student_data = student_model.get_student_by_id(id)
    if not student_data:
        return redirect(url_for('student.student_page'))

    form.id_number_year.data, form.id_number_unique.data = student_data[0].split('-')
    programs = program_model.get_programs()
    form.program.choices = [(None, 'None')] + [(program[0], program[1]) for program in programs]

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
            
        if form.program.data == "":
            form.program.data = None
            
        student_update_data = {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "gender": form.gender.data,
            "program": form.program.data,
            "year_level": form.year_level.data,
            "image_url": image_url
        }
        student_model.update_student(student_update_data, id)
        return redirect(url_for('student.student_page'))

    return render_template('student.html', form=form, programs=programs)

@student_bp.route('/delete/<id>', methods=['POST'])
def delete_student_route(id):
    db = current_app.config['db']
    student_model = StudentModel(db)
    student_data = student_model.get_student_by_id(id)
    if student_data:
        image_url = student_data[6]
        student_model.delete_student(id)
        if image_url:
            try:
                public_id = image_url.split('/')[-1].split('.')[0]
                destroy(public_id)
            except Exception as e:
                print(f"Failed to delete image: {e}")

    return redirect(url_for('student.student_page'))
