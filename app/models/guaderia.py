from config.db import db

class Guarderia(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(45), nullable = False)
    direccion = db.Column(db.String(45), nullable = False)
    telefono = db.Column(db.String(45), nullable = False)