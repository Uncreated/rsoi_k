from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, ValidationError, DateField
from wtforms.validators import Required
import re, glib

def validateEmail(form, field):
	return glib.stringEqualRegular("[a-zA-Z][a-zA-Z0-9]*@[a-zA-Z][a-zA-Z0-9]*.[a-zA-Z]+", field.data)

def validateLetters(form, field):
	string = field.data
	result = glib.getStringOnlyLetters(string)
	if ( string == result ):
		return True
	field.data = result
	return False
#	return glib.stringOnlyLetters(field.data)
	
class LoginForm(Form):
	email = TextField('Email', validators = [validateEmail, validators.Length(min=5, max=32)])
	password = PasswordField('Password', validators = [validators.Length(min=4, max=32)])
	
class SearchForm(Form):
	keyword = TextField('KeyWord', validators = [validateLetters, validators.Length(min=1, max=32)])