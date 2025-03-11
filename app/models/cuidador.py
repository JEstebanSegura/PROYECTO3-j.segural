from config.db import db

class Cuidador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    telefono = db.Column(db.String(45), nullable=False)