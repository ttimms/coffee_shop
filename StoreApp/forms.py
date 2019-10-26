from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class NewProductForm(FlaskForm):
  category = SelectField('Category: ',
                choices=[('coffee',   'Coffee'), 
                        ('food', 'Food'),
                        ('treat', 'Treat')]
              )
  name = StringField('Product Name', validators=[DataRequired()])
  price = FloatField('Price', validators=[DataRequired()])
  description = StringField('Description')
  image = FileField('Image', validators=[FileRequired()])
  submit = SubmitField('Create')
