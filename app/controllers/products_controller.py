from flask import Blueprint, render_template, request, redirect, url_for
from models.product import Product, total_calories, total_cost, profit, best_profit_product, sell_product
from models.ingredient import Ingredient
from models.product_ingredients import ProductIngredient
from config.db import db

product_blueprint = Blueprint('product_blueprint', __name__, url_prefix="/products")

@product_blueprint.route('/')
def show_products():
    products = Product.query.all()
    product_details = []
    
    for product in products:
        product_details.append({
            'product': product,
            'total_calories': total_calories(product),
            'total_cost': total_cost(product),
            'profit': profit(product)
        })
    
    best_profit_product_obj = best_profit_product(product_details)

    return render_template('show_products.html', product_details=product_details, best_profit_product=best_profit_product_obj)

@product_blueprint.route("/<int:id>", methods = ["GET"])
def get_product(id):
    product =  Product.query.get_or_404(id)
    return render_template ("prodcut.html", perro = product)

@product_blueprint.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'GET':
        return render_template('add_product.html')

    name = request.form.get("name")
    selling_price = request.form.get("selling_price")
    product_type = request.form.get("product_type")
    cup_type = request.form.get("cup_type")
    volume = request.form.get("volume")

    if not name or not selling_price or not product_type:
        return "Error: Faltan datos obligatorios"

    try:
        selling_price = float(selling_price)
    except ValueError:
        return "Error: El precio debe ser un número"

    product = Product(name=name, selling_price=selling_price, product_type=product_type, cup_type=cup_type, volume=volume)
    db.session.add(product)
    db.session.commit()
    
    return redirect(url_for('product_blueprint.show_products')) 

@product_blueprint.route('/<int:product_id>/ingredients', methods=['GET'])
def get_ingredients(product_id):
    product = Product.query.get_or_404(product_id)

    ingredients = product.ingredients
    total_calories = round(sum(ingredient.calories for ingredient in ingredients) * 0.95, 2)
    total_cost = sum(ingredient.price for ingredient in ingredients)

    all_ingredients = Ingredient.query.all()
    return render_template("product_details.html", product=product, ingredients=ingredients, all_ingredients =all_ingredients, total_calories=total_calories, total_cost=total_cost )

@product_blueprint.route('/<int:product_id>/add_ingredient', methods=['POST'])
def add_ingredient(product_id):
    ingredient_id = request.form.get("ingredient_id")

    if not ingredient_id:
        return "Error: Debe seleccionar un ingrediente"

    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return "Error: Ingrediente no encontrado"

    new_product_ingredient = ProductIngredient(product_id=product_id, ingredient_id=ingredient_id)
    db.session.add(new_product_ingredient)
    db.session.commit()
    return get_ingredients(product_id)
    
@product_blueprint.route('/<int:product_id>/remove_ingredient', methods=['POST'])
def remove_ingredient(product_id):
    ingredient_id = request.form.get("ingredient_id")

    if not ingredient_id:
        return "Error: Ingrediente no encontrado"

    product_ingredient = ProductIngredient.query.filter_by(product_id=product_id, ingredient_id=ingredient_id).first()

    if not product_ingredient:
        return "Error: Ingrediente no encontrado"

    db.session.delete(product_ingredient)
    db.session.commit()
    return get_ingredients(product_id)

@product_blueprint.route('/<int:product_id>/vender', methods=['POST'])
def try_sell_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)

        success, ingredientes_faltantes = sell_product(product)

        if not success:
            return render_template("venta_erronea.html", product=product, ingredientes_faltantes=ingredientes_faltantes)

        for ingredient in product.ingredients:
            ingredient.inventory -= 10
        
        db.session.commit()

        return render_template("venta_exitosa.html", product=product)

    except Exception as e:
        db.session.rollback()
        return "Ocurrió un error inesperado"

