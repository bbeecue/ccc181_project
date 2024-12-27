from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .college_forms import CollegeForm
from .college_models import CollegeModel

college_bp = Blueprint('college', __name__, url_prefix='/college')



@college_bp.route('/', methods=['GET', 'POST'])
def college_page():
    db = current_app.config['db']
    college_model = CollegeModel(db)

    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'College Code')  # Default to 'College Code'

    colleges = college_model.search_colleges(search_query, search_by)

    form = CollegeForm()
    return render_template('college.html', form=form, colleges=colleges)

@college_bp.route('/add', methods=['GET', 'POST'])
def add_college():
    form = CollegeForm()
    db = current_app.config['db']
    college_model = CollegeModel(db)
    colleges = college_model.get_colleges()

    if form.validate_on_submit():
        code = form.college_code.data
        name = form.college_name.data

        if college_model.college_exists(code):
            form.college_code.errors.append("College with this code already exists.")
            return render_template('college.html', form=form, colleges=colleges)

        if college_model.insert_college(code, name):
            return redirect(url_for('college.college_page'))

    return render_template('college.html', form=form, colleges=colleges)

@college_bp.route('/edit/<code>', methods=['GET', 'POST'])
def edit_college(code):
    form = CollegeForm()
    db = current_app.config['db']
    college_model = CollegeModel(db)
    college_data = college_model.fetch_college_by_code(code)
    colleges = college_model.get_colleges()

    if request.method == 'GET' and college_data:  # Populate form for editing
        form.college_code.data = college_data['code']
        form.college_name.data = college_data['name']

    if form.validate_on_submit():
        new_code = form.college_code.data
        name = form.college_name.data

        if new_code != code and college_model.college_exists(new_code):
            form.college_code.errors.append("College with this code already exists.")
            return render_template('college.html', form=form, colleges=colleges)

        if college_model.update_college(code, new_code, name):
            return redirect(url_for('college.college_page'))

    return render_template('college.html', form=form, colleges=colleges)

@college_bp.route('/delete/<code>', methods=['POST'])
def delete_college_route(code):
    db = current_app.config['db']
    college_model = CollegeModel(db)
    college_model.delete_college(code)
    return redirect(url_for('college.college_page'))
