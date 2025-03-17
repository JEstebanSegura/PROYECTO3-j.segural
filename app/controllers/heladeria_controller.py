from flask import Blueprint, render_template
from models.product import Product, best_profit_product
from models.ingredient import Ingredient

heladeria_blueprint = Blueprint('heladeria_blueprint', __name__)

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

    return render_template('index.html', products=product_details, ingredients=ingredients, best_profit_product=best_profit_product_obj)
