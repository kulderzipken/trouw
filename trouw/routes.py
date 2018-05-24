from flask import render_template, flash, redirect, url_for, request
from trouw import app, db, bcrypt
from trouw.forms import RegistrationForm, LoginForm
from trouw.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Thomas Vanneuville',
        'title': 'First one w00t',
        'content': 'Tga nog een einde machtig zien!',
        'date_posted': 'Mei 23, 2018'
    },
    {
        'author': 'Frodo',
        'title': 'WOEF',
        'content': 'Waar is men frodog?',
        'date_posted': 'Mei 23, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/fotos")
def fotos():
    return render_template('fotos.html', title = "Foto's")

@app.route("/forum")
def forum():
    return render_template('forum.html',posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name = form.name.data, email=form.email.data, password=hashed_password, amount= form.amount.data)
        db.session.add(user)
        db.session.commit()
        flash('Welkom , je kan nu inloggen!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login niet gelukt. Controleer email en wachtwoord', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = "Account")
