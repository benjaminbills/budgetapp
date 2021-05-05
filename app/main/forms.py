from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import Required, Email
from wtforms import ValidationError

class ExpenseForm(FlaskForm):

  category = SelectField('category', choices=[('Groceries','Groceries'),('Housing','Housing'),('Eat Out','Eat Out'), ('Shopping','Shopping'), ('Helping','Helping'),('Education','Education'), ('Others','Others')])
  description = StringField('Description', validators=[Required()])
  ammount = FloatField('Ammount', validators=[Required()])
  date = DateField('Date',validators=[Required()])
  submit = SubmitField('Submit')

class SalaryForm(FlaskForm):
  salary = FloatField('Salary', validators=[Required()])
  submit = SubmitField('Submit')