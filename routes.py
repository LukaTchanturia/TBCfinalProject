from flask import flash, session
from sqlalchemy import null

from extenstions import app, render_template, db, request, redirect
from models import Product, User
from forms import AddProductForm, EditProductForm, RegisterForm, LoginForm
import os
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_FOLDER = 'static'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/')
def home():
    dogs = Product.query.filter_by(adopted_by="null").all()
    return render_template('home.html', dogs=dogs)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@login_required
@app.route('/add_product', methods=["GET", "POST"])
def add_product():
    form = AddProductForm()
    if request.method == 'POST':
        file = request.files['img']
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        name = form.name.data
        img = filename
        breed = form.breed.data
        age = form.age.data
        gender = form.gender.data
        description = form.description.data
        product = Product(img=img, name=name, breed=breed, age=age, gender=gender, description=description,
                          adopted_by="null")
        db.session.add(product)
        db.session.commit()
        return redirect('/')

    return render_template('add_product.html', form=form)


@app.route('/show_details/<int:dog_id>')
def show_details(dog_id):
    selected_dog = Product.query.get_or_404(dog_id)

    return render_template('details.html', dog=selected_dog)


@login_required
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    form = EditProductForm()
    selected_dog = Product.query.get_or_404(id)
    if request.method == 'POST':
        file = request.files['img']
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        selected_dog.name = form.name.data
        selected_dog.img = filename
        selected_dog.breed = form.breed.data
        selected_dog.age = form.age.data
        selected_dog.gender = form.gender.data
        selected_dog.description = form.description.data
        db.session.commit()
        return redirect('/')
    return render_template("edit_product.html", form=form)


@login_required
@app.route("/delete/<int:id>")
def delete(id):
    selected_dog = Product.query.get(id)
    db.session.delete(selected_dog)
    db.session.commit()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("თქვენ წარმატებით დარეგისტრირდით!")
        return redirect("/login")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash("თქვენ წარმატებით შეხვედით!")
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)


@login_required
@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("თქვენ წარმატებით გახვედით ")
    return redirect("/")


@login_required
@app.route('/profile', methods=["GET", "POST"])
def profile():
    adopted_dogs = Product.query.filter_by(adopted_by=current_user.id).all()
    return render_template('profile.html', dogs=adopted_dogs)


@login_required
@app.route('/adopt/<int:dog_id>', methods=['GET', 'POST'])
def adopt_dog(dog_id):
    user_id = current_user.id
    dog = Product.query.get_or_404(dog_id)

    dog.adopted_by = user_id
    flash("თქვენ წარმატებით აიყვანეთ ძაღლი!")
    db.session.commit()
    return redirect('/')
