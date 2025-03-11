from flask import render_template, make_response
from flask_restful import Resource
from models.guaderia import Guarderia

class GuaderiaController(Resource):
    def get(self):
        guarderia = Guarderia.query.all()
        info = guarderia[0].nombre
        print(info)
        return make_response(render_template("index.html", info = info))