import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))


class User(db.Model):
    id = db.Colum(db.Integer, primary_key=True)
    name = db.Colum(db.String, unique=True)
    email = db.Colum(db.String, unique=True)
    secret_number = db.Colum(db.Integer, unique=False)
