from config.db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120), nullable = False)
    es_admin = db.Column(db.Boolean, default=False) 
    es_empleado = db.Column(db.Boolean, default=False) 