from movies_webstore import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_image.jpg")
    favorite_movies = db.Column(db.Text(), nullable=True, unique=False, default="")

    def __repr(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
