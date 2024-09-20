from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class AddStudentForm(FlaskForm):
    id_number_year = StringField('ID Number (Year)', validators=[DataRequired(), Length(min=4, max=4)])
    id_number_unique = StringField('ID Number (Unique)', validators=[DataRequired(), Length(min=4, max=4)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other')], validators=[DataRequired()])
    program = SelectField('Program', choices=[], validators=[DataRequired()])  # Choices will be populated dynamically
    year_level = IntegerField('Year Level', validators=[DataRequired(), NumberRange(min=1, max=4)])
    submit = SubmitField('Add Student')