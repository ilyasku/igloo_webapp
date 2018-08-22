from flask_wtf import FlaskForm
from wtforms import (FloatField, SelectField, TextField,                    
                     IntegerField, SubmitField)
from wtforms.validators import DataRequired, NumberRange, ValidationError

def _no_input_allowed(form, field):
    if len(field.data) > 0:
        raise ValidationError("Please do not give us this info!")

class RunRWMCForm(FlaskForm):    
    start_pos = FloatField('Start Position [mm] (-1 for random)',
                           validators=[DataRequired()], default=25)
    T_min = FloatField('Minimum Temperature [C]', validators=[DataRequired()], default=12)
    T_max = FloatField('Maximum Temperature [C]', validators=[DataRequired()], default=32)
    T_rear = FloatField('Rearing Temperature [C]', validators=[DataRequired()], default=25)
    length = FloatField('Length [mm]', validators=[DataRequired()], default=50)
    duration = FloatField('Walk Duration [s]',
                          validators=[DataRequired("Floating point number in range [0.0, 7200.0] required."),
                                      NumberRange(0.0, 7200,
                                                  'Needs to be in range [0.0, 7200.0].')],
                          default=5)
    frames_per_sec = IntegerField('Frames per Sec.',
                                  validators=[DataRequired("Floating point number in range [1.0, 100.0] required."),
                                              NumberRange(1.0, 100,
                                                          'Needs to be in range [1.0, 100.0].')],
                                  default=10)
    simulation_type = SelectField('Simulation Type', choices=[('interpolate', 'Interpolate'),
                                                              ('onData', 'On Data')])
    n_flies = IntegerField('Number of Flies/Simulations',
                           validators=[DataRequired("Integer in range [1, 100] required."),
                                       NumberRange(1, 100,
                                                   'Maximum 100 Flies allowed.' +
                                                   ' Download IGLOO code and run it ' +
                                                   'on your machine if you need larger n.')],
                           default=1)

    # hidden honeypot field
    phone_number_a453c45163 = TextField('We are not that interested in your phone number!',
                                        validators=[_no_input_allowed])
    
    submit = SubmitField('Submit Job')
