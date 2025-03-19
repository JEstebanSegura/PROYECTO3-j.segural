from config.db import db
from models.ingredient import Ingredient
from models.product_ingredients import ProductIngredient
from config.marshmallow import marshmallow

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    cup_type = db.Column(db.String(50), nullable=False)
    volume = db.Column(db.String(50), nullable=False)
    
    ingredients = db.relationship('Ingredient', secondary='product_ingredient', backref="products")
   
def total_calories(product):
    ingredients = product.ingredients
    if product.product_type == "cup":
        return sum(ingredient.calories for ingredient in ingredients)*0.95
    elif product.product_type == "milkshake":
        return sum(ingredient.calories for ingredient in ingredients)

def total_cost(product):
    ingredients = product.ingredients
    if product.product_type == "cup":
        return sum(ingredient.price for ingredient in ingredients) +200
    elif product.product_type == "milkshake":
        return sum(ingredient.price for ingredient in ingredients) + 500

def profit(product):
    ingredients = product.ingredients
    return  product.selling_price - sum(ingredient.price for ingredient in ingredients)

def best_profit_product(product_details):
    best_profit_product = None
    max_profit = -float('inf')

    for detail in product_details:
        profit = detail['profit']

        if profit > max_profit:
            max_profit = profit
            best_profit_product = detail['product']

    return best_profit_product

def sell_product(product):
    if not product:
        return False, []

    ingredientes_faltantes = []

    for ingredient in product.ingredients:
        if ingredient.inventory <= 0:
            ingredientes_faltantes.append(ingredient.name)
        elif ingredient.inventory < 10:
            ingredientes_faltantes.append(f"{ingredient.name}")

    if ingredientes_faltantes:
        return False,  ingredientes_faltantes

    return True, []


class ProductSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_relationships = True
        include_fk = True

