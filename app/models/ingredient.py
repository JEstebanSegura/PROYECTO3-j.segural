from config.db import db

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    is_vegetarian = db.Column(db.Boolean, nullable=False)
    ingredient_type = db.Column(db.String(50), nullable=False)  # Para diferenciar entre Base y Topping
    flavor = db.Column(db.String(50), nullable=True)

    def is_healthy(self):
        return self.calories < 100 and self.is_vegetarian

    def suply(self):
        self.inventory += 5
        return self
    