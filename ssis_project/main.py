from flask import Blueprint, render_template, current_app, request, redirect, url_for
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return render_template("base.html")

"""

@main_bp.route('/college')
def college_form():
    return render_template("college.html")

@main_bp.route('/program')
def program_form():
    return render_template("program.html")
    
"""