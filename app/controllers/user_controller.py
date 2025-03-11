
from flask import render_template, request, make_response
from flask_login import login_user, current_user, logout_user
from flask_restful import Resource
from models.user import User
from config.auth import login_manager

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(user_id)

class login(Resource):
    def get(self):
        return make_response(render_template("login.html"))

class auth(Resource):
    def get(self):
        username = request.args.get("username")
        password =  request.args.get("password")
        if request.args.get("username") == None:
            raise ValueError("No tiene el parametro de name")
        if request.args.get("password") ==None:
            raise ValueError("No tiene el parametro de name")
        user = User.query.filter_by(username = username, password = password).first()
        
        if user:
            login_user(user)
            return make_response(render_template ("dashboard.html"))
            
        return make_response(render_template("login.html"))

class auth_profile(Resource):
    def get(self):
        return f'datos: {current_user.username}'

class logout(Resource):
    def get(self):
        logout_user()
        return make_response(render_template("login.html"))