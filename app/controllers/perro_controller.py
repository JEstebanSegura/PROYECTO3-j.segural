from flask import render_template, make_response
from flask_login import current_user, login_required
from flask_restful import Resource
from models.perro import Perro

class PerroController(Resource):
    @login_required
    def get(self):
        if current_user.es_admin:
            perros = Perro.query.all()
            return make_response(render_template("admin_dashboard.html", perros=perros))
        else:
            return make_response(render_template("dashboard.html", username=current_user.username))

class PerroLassieController(Resource):
    def get(self):
        perro_lassie = Perro.query.filter_by(nombre='Lassie').all()
        info = len(perro_lassie)
        return make_response(render_template("perros_lasie.html", info = info))