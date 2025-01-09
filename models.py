from extenstions import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    breed = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    adopted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="guest")

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    dogs = [{'name': 'პაბლო', "img": "dog1.jpeg", 'breed': 'გერმანული ნაგაზი', 'age': '5', 'gender': 'ხვადი',
             'description': 'პაბლო აცრილი და კეთილი ძაღლია. მან ყველა საჭირო პროცედურა გაიარა ჩვენთან და მზადაა, რომ მზრუნველი და მოსიყვარულე ოჯახში მხიარულება შეიტანოს',
             "adopted_by": "null"}]
    with app.app_context():
        db.create_all()
        for dog in dogs:
            new_dog = Product(name=dog["name"], img=dog["img"], breed=dog["breed"], age=dog["age"],
                              gender=dog["gender"], description=dog["description"], adopted_by=dog["adopted_by"])
            db.session.add(new_dog)
        user = User(username="kaciadamiani", password="paroli123")
        admin = User(username="admin", password="admin123123", role="admin")
        db.session.add(user)
        db.session.add(admin)
        db.session.commit()
