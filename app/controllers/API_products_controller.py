from flask import Blueprint, jsonify
from flask_login import login_user, current_user, login_required
from models.product import Product, ProductSchema, total_calories, total_cost, profit,sell_product
from config.db import db
from config.auth import login_manager
from models.user import User

API_product_blueprint = Blueprint('API_product_blueprint', __name__, url_prefix="/api/products")

product_schema =ProductSchema()
products_schema =ProductSchema(many = True)

@login_manager.user_loader
def load_user(user_id:int):
    return User.query.get(user_id)

@API_product_blueprint.route('/')
def show_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products))

@API_product_blueprint.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    print(product)
    return jsonify(product_schema.dump(product))

@API_product_blueprint.route('/name/<string:product_name>', methods=['GET'])
def get_product_by_name(product_name):
    product = Product.query.filter_by(name=product_name).first()

    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product_schema.dump(product))

@API_product_blueprint.route('/calories/<int:product_id>', methods=['GET'])
def get_product_calories(product_id):
    product = Product.query.get_or_404(product_id)

    calories = total_calories(product)

    return jsonify({"product_id": product.id, "name": product.name, "calories": calories})

@API_product_blueprint.route('/profit/<int:product_id>', methods=['GET'])
def get_product_profit(product_id):
    product = Product.query.get_or_404(product_id)

    product_profit = profit(product)

    return jsonify({"product_id": product.id, "name": product.name, "profit": product_profit})

@API_product_blueprint.route('/cost/<int:product_id>', methods=['GET'])
def get_product_cost(product_id):
    product = Product.query.get_or_404(product_id)

    product_cost = total_cost(product)

    return jsonify({"product_id": product.id, "name": product.name, "cost": product_cost})


@API_product_blueprint.route('/sell/<int:product_id>', methods=['POST'])
def sell_product_route(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        success, ingredientes_faltantes = sell_product(product)

        if not success:
            return jsonify({
                "success": False,
                "message": "No se pudo completar la venta",
                "missing_ingredients": ingredientes_faltantes
            }), 400 

        for ingredient in product.ingredients:
            ingredient.inventory -= 10
        
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Venta exitosa",
            "product": {
                "id": product.id,
                "name": product.name,
                "selling_price": product.selling_price
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Ocurrió un error inesperado",
            "message": str(e)
        }), 500

