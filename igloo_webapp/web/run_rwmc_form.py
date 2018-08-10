from flask_wtf import FlaskForm
from wtforms import (FloatField, SelectField,
                     IntegerField, SubmitField)
from wtforms.validators import DataRequired


class RunRWMCForm(FlaskForm):    
    start_pos = FloatField('Start Position [mm]', validators=[DataRequired()])
    T_min = FloatField('Minimum Temperature [C]', validators=[DataRequired()])
    T_max = FloatField('Maximum Temperature [C]', validators=[DataRequired()])
    T_rear = FloatField('Rearing Temperature [C]', validators=[DataRequired()])
    length = FloatField('Length [mm]', validators=[DataRequired()])
    duration = FloatField('Walk Duration [s]', validators=[DataRequired()])
    frames_per_sec = IntegerField('Frames per Sec.', validators=[DataRequired()])
    simulation_type = SelectField('Simulation Type', choices=[('onData', 'On Data'),
                                                              ('interpolate', 'Interpolate')])
    submit = SubmitField('Submit Job')
