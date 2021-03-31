from flask_wtf import FlaskForm
from wtforms import StringField


class TitleLink(FlaskForm):
    title = StringField('title')
    link = StringField('link')


