from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from trouw.models import User

class RegistrationForm(FlaskForm):
    name = StringField('Voor- en Achternaam',validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    amount = RadioField('Aantal Personen', choices=[('0', 'Ik kan niet komen'),('1', 'Ik kom'), ('2', 'Ik kom met partner')], validators =[DataRequired()])
    password = PasswordField('Maak een Wachtwoord', validators =[DataRequired()])
    confirm_password = PasswordField('Confirmeer Wachtwoord', validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Voltooi')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=name.data).first()
        if user:
            raise ValidationError('Naam Bestaal Al')

    def validate_email(self, email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Deze mail bestaat al. Gebruik een ander mailadres')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators =[DataRequired()])
    remember = BooleanField('Remember Me')
    submit= SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    name = StringField('Naam',validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    amount = RadioField('Aantal Personen', choices=[('0', 'Ik kan niet komen'),('1', 'Ik kom'), ('2', 'Ik kom met partner')], validators =[DataRequired()])
    picture = FileField('Verander Profielfoto', validators=[FileAllowed(['jpg','png'])])
    submit= SubmitField('Update')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user= User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Deze mail bestaat al. Gebruik een ander mailadres')

    def validate_username(self, username):
        user = User.query.filter_by(username=name.data).first()
        if user:
            raise ValidationError('Naam Bestaal Al')

class PostForm(FlaskForm):
    title = StringField('onderwerp', validators=[DataRequired()])
    content = TextAreaField('Tekst', validators=[DataRequired()])
    submit= SubmitField('Post')