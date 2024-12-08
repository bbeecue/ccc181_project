from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, IntegerField, RadioField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp


class StudentForm(FlaskForm):
    
    id_number_year = StringField('ID Number (Year)', validators=[DataRequired(message="ID Number (Year) is required."),
            Regexp(r'^\d{4}$', message="Year must be a 4-digit number."), Length(min=4, max=4)])
    
    id_number_unique = StringField('ID Number (Unique)', validators=[DataRequired(message="ID Number (Unique) is required."),
            Regexp(r'^\d{4}$', message="Unique Number must be a 4-digit number."), Length(min=4, max=4)])
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other')], validators=[DataRequired()])
    program = SelectField('Program', choices=[])
    year_level = IntegerField('Year Level', validators=[DataRequired(), NumberRange(min=1, max=4)])
    submit = SubmitField('Submit')
    student_image = FileField('Upload Image:')
