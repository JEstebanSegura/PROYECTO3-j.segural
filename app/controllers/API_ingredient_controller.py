from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, current_user, login_required
from models.ingredient import Ingredient, IngredientSchema
from config.db import db

from config.auth import login_manager
from models.user import User

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(user_id)

API_ingredient_blueprint = Blueprint('API_ingredient_blueprint', __name__, url_prefix="/api/ingredients")

ingredient_schema =IngredientSchema()
ingredients_schema =IngredientSchema(many = True)

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(user_id)

@API_ingredient_blueprint.route('/')
def show_ingredient():
    ingredients = Ingredient.query.all()
    return jsonify(ingredients_schema.dump(ingredients))

@API_ingredient_blueprint.route('/<int:ingrefient_id>', methods=['GET'])
def get_ingredient(ingrefient_id):
    product = Ingredient.query.get_or_404(ingrefient_id)
    print(product)
    return jsonify(ingredient_schema.dump(product))

@API_ingredient_blueprint.route('/name/<string:ingredient_name>', methods=['GET'])
def get_ingredient_by_name(ingredient_name):
    product = Ingredient.query.filter_by(name=ingredient_name).first()

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(ingredient_schema.dump(product))

@API_ingredient_blueprint.route('/healthy/<int:ingrefient_id>', methods=['GET'])
def get_ingredient_is_healthy(ingrefient_id):
    ingredient = Ingredient.query.get_or_404(ingrefient_id)

    is_healthy = ingredient.is_healthy()

    return jsonify({
        "ingredient_id": ingredient.id,
        "name": ingredient.name,
        "is_healthy": is_healthy
    })

@API_ingredient_blueprint.route('/supply/<int:ingredient_id>', methods=['PATCH'])
def supply_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)

    ingredient.suply()
    db.session.commit()

    return jsonify({
        "ingredient_id": ingredient.id,
        "name": ingredient.name,
        "new_inventory": ingredient.inventory
    }), 200










@API_ingredient_blueprint.route("/<int:id>/suply", methods = ["POST"])
@login_required
def suplay_ingredient(id):

    if not (current_user.es_admin or current_user.es_empleado):
        return render_template('acceso_denegado.html')
    
    ingredient = Ingredient.query.get_or_404(id)
    ingredient.suply()
    
    db.session.commit()
        
    return redirect(url_for('ingredient_blueprint.show_ingredient'))