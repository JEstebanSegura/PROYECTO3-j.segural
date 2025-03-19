from controllers.products_controller import product_blueprint
from controllers.ingredient_controller import ingredient_blueprint
from controllers.heladeria_controller import heladeria_blueprint
from controllers.user_controller  import user_blueprints
from controllers.API_products_controller import API_product_blueprint
from controllers.API_ingredient_controller import API_ingredient_blueprint


def register_routes(app):
    app.register_blueprint(product_blueprint)
    app.register_blueprint(ingredient_blueprint)
    app.register_blueprint(heladeria_blueprint)
    app.register_blueprint(user_blueprints)
    app.register_blueprint(API_product_blueprint)
    app.register_blueprint(API_ingredient_blueprint)
