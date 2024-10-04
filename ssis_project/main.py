from flask import Blueprint, render_template, current_app, request, redirect, url_for
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return redirect(url_for('student.student_page'))


