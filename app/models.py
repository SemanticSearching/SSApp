"""
define the database structure
"""
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY


class Paper(db.Model):
    title = db.Column(db.String, index=True)
    link = db.Column(db.String, index=True)
    seg = db.Column(db.String, index=True)
    e1 = db.Column(ARRAY(db.FLOAT), index=True)
    e2 = db.Column(ARRAY(db.FLOAT), index=True)
    e3 = db.Column(ARRAY(db.FLOAT), index=True)
    e4 = db.Column(ARRAY(db.FLOAT), index=True)
    id = db.Column(db.Integer, index=True, unique=True, primary_key=True)

    def __repr__(self):
        return'<Paper {}>'.format(self.title)


# ...
class User(UserMixin, db.Model):
    # ...
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    # user_email = db.Column(db.Integer, index=True, unique=True, primary_key=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



