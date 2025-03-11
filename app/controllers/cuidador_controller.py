from flask import render_template, make_response
from flask_restful import Resource
from models.cuidador import Cuidador
from models.perro import Perro

class PerrosDeMarioController(Resource):
    def get(self):
        mario = Cuidador.query.filter_by(nombre='Mario').first()
        perros_mario = Perro.query.filter(Perro.peso < 3).update({"id_cuidador": mario.id})
        return make_response(render_template("perros_mario.html", info = perros_mario))