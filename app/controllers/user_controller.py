
from flask import render_template, request, make_response, Blueprint, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from config.auth import login_manager
from models.user import User

login_manager.login_view = "auth.login" 
user_blueprints = Blueprint("auth", __name__, url_prefix = "/auth")

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(user_id)

@user_blueprints.route("/login")
def login():
    return render_template('login.html')

@user_blueprints.route("/auth", methods=["GET", "POST"])
def auth():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return make_response(render_template("login.html", error="Faltan credenciales"))

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        login_user(user)
        return redirect(url_for("heladeria_blueprint.menu"))
    
    flash("Error en sus credenciales o no se enceuntra el usuario", "error")
    return redirect(url_for('auth.login'))


@user_blueprints.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
