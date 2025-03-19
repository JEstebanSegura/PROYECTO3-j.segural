from flask import Blueprint, render_template
from models.product import Product, best_profit_product
from flask_login import login_required, current_user
from models.ingredient import Ingredient
from config.auth import login_manager
from models.user import User

heladeria_blueprint = Blueprint('heladeria_blueprint', __name__)

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(user_id)

@heladeria_blueprint.route("/menu")
@login_required
def menu():
    return render_template(
        "menu.html",
        username=current_user.username,
        es_admin=current_user.es_admin,
        es_empleado=current_user.es_empleado
    )

@heladeria_blueprint.route('/index')
def index():
    products = Product.query.all()
    product_details = []
    
    for product in products:
        
        ingredients = product.ingredients

        total_calories = sum(ingredient.calories for ingredient in ingredients)
        total_cost = sum(ingredient.price for ingredient in ingredients)
        profit = product.selling_price - total_cost

        product_details.append({
            'product': product,
            'total_calories': total_calories,
            'total_cost': total_cost,
            'profit': profit
        })

    best_profit_product_obj = best_profit_product(product_details)
    ingredients = Ingredient.query.all()

    # Determinar el rol del usuario autenticado
    user_role = "cliente"  # Por defecto, usuario no autenticado
    if current_user.is_authenticated:
        if current_user.es_admin:
            user_role = "admin"
        elif current_user.es_empleado:
            user_role = "empleado"

    return render_template(
        'sell.html',
        products=product_details,
        best_profit_product=best_profit_product_obj,
        current_user=current_user,
        user_role = user_role
    )


