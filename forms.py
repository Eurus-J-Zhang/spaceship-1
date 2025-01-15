from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea

# Here is for Prolific ID and gender and age
class DemographicInfo(FlaskForm):
    id = StringField('Prolific ID', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('M','Male'),('F','Female'),('O','Others')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=80)])

eleven_point_scale = [(str(i), f'Opt{i}') for i in range(11)]

# Here is the first emotion check
class EmotionForm(FlaskForm):
    despair = RadioField('Despair', choices=eleven_point_scale, validators=[DataRequired()])
    anxiety = RadioField('Anxiety', choices=eleven_point_scale, validators=[DataRequired()])
    irritation = RadioField('Irritation', choices=eleven_point_scale, validators=[DataRequired()])
    rage = RadioField('Rage', choices=eleven_point_scale, validators=[DataRequired()])
    shame = RadioField('Shame', choices=eleven_point_scale, validators=[DataRequired()]) 
    guilt = RadioField('Guilt', choices=eleven_point_scale, validators=[DataRequired()])  

    
    feedback = StringField('',validators=[DataRequired()],widget=TextArea())