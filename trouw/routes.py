import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from trouw import app, db, bcrypt
from trouw.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from trouw.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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

@app.route("/forum", methods=['GET', 'POST'])
@login_required
def forum():
    form = PostForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('forum'))
    return render_template('forum.html',posts=posts, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name = form.name.data, email=form.email.data, password=hashed_password,
                    amount= form.amount.data)
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file    
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.amount = form.amount.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.amount.data = current_user.amount
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = "Account", image_file= image_file, form=form)
