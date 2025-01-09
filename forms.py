from wtforms.validators import DataRequired, EqualTo, NumberRange
from extenstions import FlaskForm
from wtforms.fields import StringField, IntegerField, FileField, SubmitField, SelectField, PasswordField


class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    img = FileField('Image', validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1, max=32)])
    gender = SelectField('Gender', validators=[DataRequired()], choices=["ხვადი", "ძუ"])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    img = FileField('Image', validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat your password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Please insert a name")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("შესვლა")
