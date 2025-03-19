from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from models.ingredient import Ingredient
from config.db import db

from config.auth import login_manager
from models.user import User

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(user_id)

ingredient_blueprint = Blueprint('ingredient_blueprint', __name__, url_prefix="/ingredients")

@ingredient_blueprint.route('/')
@login_required
def show_ingredient():
    ingredients = Ingredient.query.all()
    return render_template('show_ingredients.html', ingredients=ingredients)

@ingredient_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_ingredient():

    if not current_user.es_admin:
        return render_template('acceso_denegado.html')
    
    if request.method == 'GET':
        return render_template('add_ingredients.html')

    name = request.form.get("name")
    price = request.form.get("price")
    calories = request.form.get("calories")
    inventory = request.form.get("inventory")
    is_vegetarian = request.form.get("is_vegetarian")
    ingredient_type = request.form.get("ingredient_type")
    flavor = request.form.get("flavor")

    if not all([name, price, calories, inventory, ingredient_type, flavor]):
        return "Error: Faltan datos obligatorios", 400

    try:
        price = float(price)
        if price < 0:
            return "Error: El precio no puede ser negativo", 400
    except ValueError:
        return "Error: El precio debe ser un número", 400

    try:
        calories = int(calories)
        if calories < 0:
            return "Error: Las calorías no pueden ser negativas", 400
    except ValueError:
        return "Error: Las calorías deben ser un número entero", 400

    try:
        inventory = int(inventory)
        if inventory < 0:
            return "Error: El inventario no puede ser negativo", 400
    except ValueError:
        return "Error: El inventario debe ser un número entero", 400

    if is_vegetarian == "1":
        is_vegetarian = True
    elif is_vegetarian == "0":
        is_vegetarian = False
    else:
        return "Error: Valor inválido para is_vegetarian", 400

    ingredient = Ingredient(name=name, price=price, calories=calories, inventory=inventory, is_vegetarian=is_vegetarian, ingredient_type=ingredient_type, flavor=flavor)
    db.session.add(ingredient)
    db.session.commit()

    return redirect(url_for('ingredient_blueprint.show_ingredient'))

@ingredient_blueprint.route("/<int:id>/suply", methods = ["POST"])
@login_required
def suplay_ingredient(id):

    if not (current_user.es_admin or current_user.es_empleado):
        return render_template('acceso_denegado.html')
    
    ingredient = Ingredient.query.get_or_404(id)
    ingredient.suply()
    
    db.session.commit()
        
    return redirect(url_for('ingredient_blueprint.show_ingredient'))