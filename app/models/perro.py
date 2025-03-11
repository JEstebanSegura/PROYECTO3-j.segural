from config.db import db

class Perro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    raza = db.Column(db.String(45), nullable=False)
    edad = db.Column(db.String(45), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    id_cuidador = db.Column(db.Integer, db.ForeignKey('cuidador.id'), nullable=False)