from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

class CollegeForm(FlaskForm):
    
    college_code = StringField('College Code', validators=[DataRequired(message="College code is required."),
            Regexp(r'^[A-Z]+$', message="College code must contain only capital letters.")])
    
    college_name = StringField('College Name', validators=[DataRequired(message="College name is required."),
            Regexp(r'^[A-Za-z\s]+$', message="College name must contain only letters.")])
    