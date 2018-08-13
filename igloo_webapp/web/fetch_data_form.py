from flask_wtf import FlaskForm
from wtforms import (SelectField, IntegerField, SubmitField)
from wtforms.validators import DataRequired


class FetchDataForm(FlaskForm):
    job_id = IntegerField('Job ID', validators=[DataRequired()])    
    submit = SubmitField('Fetch Data')
