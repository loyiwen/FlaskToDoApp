from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired

class AssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    module_code = StringField('Module Code', validators=[DataRequired()])
    date = DateField('Deadline Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Deadline Time', format='%H:%M', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')
    