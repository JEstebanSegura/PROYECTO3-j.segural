from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_restful import Api
from config.config import Config
from config.db import db
from config.auth import login_manager
from controllers.guarderia_controller import GuaderiaController
from controllers.cuidador_controller import PerrosDeMarioController
from controllers.perro_controller import PerroLassieController
from controllers.perro_controller import PerroController
from controllers.user_controller import *

app = Flask(__name__, template_folder = "views")

app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
api = Api (app)

@app.route("/")
def home(): 
    return "ok"

api.add_resource(PerroController, '/perro')
api.add_resource(login, "/login")
api.add_resource(auth, "/auth")
api.add_resource(auth_profile, "/auth/profile")
api.add_resource(logout, "/logout")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)