from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .college_forms import CollegeForm
from .college_models import fetch_all_colleges, search_colleges, insert_college, update_college, delete_college, fetch_college_by_code, college_exists

college_bp = Blueprint('college', __name__, url_prefix='/college')

@college_bp.route('/', methods=['GET', 'POST'])
def college_page():
    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'College Code')  # Default to 'College Code'

    colleges = search_colleges(search_query, search_by)

    form = CollegeForm()
    return render_template('college.html', form=form, colleges=colleges)

@college_bp.route('/add', methods=['GET', 'POST'])
def add_college():
    form = CollegeForm()
    colleges = fetch_all_colleges()

    if form.validate_on_submit():
        code = form.college_code.data
        name = form.college_name.data

        if college_exists(code):
            form.college_code.errors.append("College with this code already exists.")
            return render_template('college.html', form=form, colleges=colleges)

        if insert_college(code, name):
            return redirect(url_for('college.college_page'))

    return render_template('college.html', form=form, colleges=colleges)

@college_bp.route('/edit/<code>', methods=['GET', 'POST'])
def edit_college(code):
    form = CollegeForm()
    college_data = fetch_college_by_code(code)
    colleges = fetch_all_colleges()

    if request.method == 'GET':  # Populate form for editing
        form.college_code.data = college_data['code']
        form.college_name.data = college_data['name']

    if form.validate_on_submit():
        new_code = form.college_code.data
        name = form.college_name.data

        if new_code != code and college_exists(new_code):
            form.college_code.errors.append("College with this code already exists.")
            return render_template('college.html', form=form, colleges=colleges)

        if update_college(code, new_code, name):
            return redirect(url_for('college.college_page'))

    return render_template('college.html', form=form, colleges=colleges)

@college_bp.route('/delete/<code>', methods=['POST'])
def delete_college_route(code):
    delete_college(code)
    return redirect(url_for('college.college_page'))
