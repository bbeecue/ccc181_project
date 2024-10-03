from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Regexp

class ProgramForm(FlaskForm):
    
    program_code = StringField('Program Code', validators=[DataRequired(message="Program code is required."),
            Regexp(r'^[A-Za-z\s]+$', message="College code must contain only letters.")])
    
    program_name = StringField('Program Name', validators=[DataRequired(message="Program name is required."),
            Regexp(r'^[A-Za-z\s]+$', message="College name must contain only letters.")])
    
    college_code = SelectField('College Code', choices=[], validators=[DataRequired()])
    
    