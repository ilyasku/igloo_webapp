from flask_wtf import FlaskForm
from wtforms import (SelectField, IntegerField, SubmitField)
from wtforms.validators import DataRequired


class FetchDataForm(FlaskForm):
    job_digest = IntegerField('Job Hash', validators=[DataRequired()])    
    submit = SubmitField('Fetch Data')
