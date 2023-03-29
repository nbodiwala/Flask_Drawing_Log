from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    project_num = StringField('Project Number', validators=[DataRequired(), Length(min=9, max=9)])
    submit = SubmitField('Search')

