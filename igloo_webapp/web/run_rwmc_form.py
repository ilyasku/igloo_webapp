from flask_wtf import FlaskForm
from wtforms import (FloatField, SelectField,
                     IntegerField, SubmitField)
from wtforms.validators import DataRequired, NumberRange


class RunRWMCForm(FlaskForm):    
    start_pos = FloatField('Start Position [mm] (-1 for random)',
                           validators=[DataRequired()], default=25)
    T_min = FloatField('Minimum Temperature [C]', validators=[DataRequired()], default=12)
    T_max = FloatField('Maximum Temperature [C]', validators=[DataRequired()], default=32)
    T_rear = FloatField('Rearing Temperature [C]', validators=[DataRequired()], default=25)
    length = FloatField('Length [mm]', validators=[DataRequired()], default=50)
    duration = FloatField('Walk Duration [s]',
                          validators=[DataRequired(),
                                      NumberRange(0.0, 3600,
                                                  'Needs to be in range [0.0, 3600.0].')],
                          default=5)
    frames_per_sec = IntegerField('Frames per Sec.',
                                  validators=[DataRequired(),
                                              NumberRange(1.0, 100,
                                                          'Needs to be in range [1.0, 100.0].')],
                                  default=10)
    simulation_type = SelectField('Simulation Type', choices=[('interpolate', 'Interpolate'),
                                                              ('onData', 'On Data')])
    n_flies = IntegerField('Number of Flies/Simulations',
                           validators=[DataRequired(),
                                       NumberRange(0, 100,
                                                   'Maximum 100 Flies allowed.' +
                                                   ' Download IGLOO code and run it ' +
                                                   'on your machine if you need larger n.')],
                           default=1)
    submit = SubmitField('Submit Job')
