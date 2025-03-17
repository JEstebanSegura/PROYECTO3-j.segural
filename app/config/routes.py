from controllers.home_controller import home_blueprint
from controllers.products_controller import product_blueprint
from controllers.ingredient_controller import ingredient_blueprint
from controllers.heladeria_controller import heladeria_blueprint

def register_routes(app):
    app.register_blueprint(home_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(ingredient_blueprint)
    app.register_blueprint(heladeria_blueprint)
