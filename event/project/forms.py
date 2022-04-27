from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,RadioField,IntegerField


class FilterForm(FlaskForm):
    criteria = SelectField("Select",choices=[("","Select..."),("country","Country"),("state","State"),("keyword","Keyword")])
    filter_word=StringField("Enter text")
    geo=RadioField('Use My Location',choices=[("1","My Location")])
    radius=IntegerField()
    # from_date=StringField("Enter text")

