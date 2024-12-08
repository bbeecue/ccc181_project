from flask import Blueprint, render_template, current_app, request, redirect, url_for
from .program_forms import ProgramForm
from .program_models import (
    get_colleges,
    get_programs,
    get_program,
    add_program,
    update_program,
    delete_program,
    existing_program
)

program_bp = Blueprint('program', __name__, url_prefix='/program')

@program_bp.route('/', methods=['GET', 'POST'])
def program_page():
    db = current_app.config['db']
    colleges = get_colleges(db)
    search_query = request.args.get('search', '')
    search_by = request.args.get('search_by', 'Program Code')
    programs = get_programs(db, search_query, search_by)

    form = ProgramForm()
    form.college_code.choices = [(college[0], college[1]) for college in colleges]
    
    return render_template('program.html', form=form, programs=programs)

@program_bp.route('/add', methods=['GET', 'POST'])
def add_program_route():
    db = current_app.config['db']
    form = ProgramForm()
    colleges = get_colleges(db)
    programs = get_programs(db)

    form.college_code.choices = [(college[0], college[1]) for college in colleges]

    if form.validate_on_submit():
        program_code = form.program_code.data
        program_name = form.program_name.data
        college_code = form.college_code.data

        if existing_program(db, program_code):
            form.program_code.errors.append("Program with this code already exists.")
            return render_template('program.html', form=form, programs=programs, colleges=colleges)

        try:
            add_program(db, program_code, program_name, college_code)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('program.html', form=form, programs=programs, colleges=colleges)

        return redirect(url_for('program.program_page'))

    return render_template('program.html', form=form, programs=programs, colleges=colleges)

@program_bp.route('/edit/<program_code>', methods=['GET', 'POST'])
def edit_program(program_code):
    db = current_app.config['db']
    form = ProgramForm()
    program_data = get_program(db, program_code)
    colleges = get_colleges(db)
    programs = get_programs(db)

    form.college_code.choices = [(college[0], college[1]) for college in colleges]

    if request.method == 'GET':
        form.program_code.data = program_data[0]
        form.program_name.data = program_data[1]
        form.college_code.data = program_data[2]

    if form.validate_on_submit():
        new_program_code = form.program_code.data
        program_name = form.program_name.data
        college_code = form.college_code.data

        try:
            update_program(db, program_code, new_program_code, program_name, college_code)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('program.html', form=form, programs=programs, colleges=colleges)

        return redirect(url_for('program.program_page'))

    return render_template('program.html', form=form, programs=programs, colleges=colleges)

@program_bp.route('/delete/<program_code>', methods=['POST'])
def delete_program_route(program_code):
    db = current_app.config['db']
    try:
        delete_program(db, program_code)
    except Exception as e:
        print(f"Error deleting program: {e}")
    return redirect(url_for('program.program_page'))
