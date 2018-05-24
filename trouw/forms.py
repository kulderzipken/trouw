from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from trouw.models import User

class RegistrationForm(FlaskForm):
    name = StringField('Naam',validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    amount = RadioField('Aantal Personen', choices=[('0', 'Ik kan niet komen'),('1', 'Ik kom'), ('2', 'Ik kom met partner')], validators =[DataRequired()])
    food = RadioField('Aantal Veggies?', choices=[('0', 'Geen vegetarische maaltijd'),('1', '1 Vegetarische Maaltijd'), ('2', '2 Vegetarische Maaltijden')], validators =[DataRequired()])
    password = PasswordField('Maak een Wachtwoord', validators =[DataRequired()])
    confirm_password = PasswordField('Confirmeer Wachtwoord', validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Sign Up')
    
    def validate_email(self, email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Deze mail bestaat al. Gebruik een ander mailadres')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators =[DataRequired()])
    remember = BooleanField('Remember Me')
    submit= SubmitField('Login')

