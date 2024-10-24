from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    module_code = StringField('Module Code', validators=[DataRequired()])
    deadline = DateField('Deadline', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    is_complete = BooleanField('Is Complete')
    submit = SubmitField('Submit')