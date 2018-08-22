from flask_wtf import FlaskForm
from wtforms import (SelectField, TextField, SubmitField)
from wtforms.validators import DataRequired


class FetchDataForm(FlaskForm):
    job_digest = TextField('Job Hash', validators=[DataRequired()])    
    submit = SubmitField('Fetch Data')
