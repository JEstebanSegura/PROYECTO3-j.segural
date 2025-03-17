import unittest
from app.models.ingredient import Ingredient
from app.models.product import Product, sell_product


class TestHeladeria(unittest.TestCase):
    def test_is_healthy(self):
        ingrediente = Ingredient(name="Fresa", calories=50, price=0.5)
        self.assertTrue(ingrediente.calories < 200, "El ingrediente no es sano")

    def test_suply(self):
        ingrediente = Ingredient(name="Leche", inventory=10)
        ingrediente.inventory += 50  # Simula el abastecimiento
        self.assertEqual(ingrediente.inventory, 60, "El abastecimiento no se realizó correctamente")

    def test_total_calories(self):
        ingrediente1 = Ingredient(name="Fresa", calories=50)
        ingrediente2 = Ingredient(name="Leche", calories=100)
        total_calories = ingrediente1.calories + ingrediente2.calories
        self.assertEqual(total_calories, 150, "Error en el cálculo de calorías")


    def test_total_cost(self):
        ingrediente1 = Ingredient(name="Fresa", price=0.5)
        ingrediente2 = Ingredient(name="Leche", price=1.0)
        total_cost = ingrediente1.price + ingrediente2.price
        self.assertEqual(total_cost, 1.5, "Error en el cálculo de costo")

    def test_profit(self):
        producto = Product(name="Malteada de Chocolate", selling_price=5.0)
        costo = 2.0
        rentabilidad = producto.selling_price - costo
        self.assertEqual(rentabilidad, 3.0, "Error en el cálculo de rentabilidad")

    def test_best_profit_product(self):
        productos = [
            {"name": "Helado de Vainilla", "profit": 2.0},
            {"name": "Malteada de Chocolate", "profit": 3.0},
            {"name": "Helado de Fresa", "profit": 1.5}
        ]
        best_product = max(productos, key=lambda x: x["profit"])
        self.assertEqual(best_product["name"], "Malteada de Chocolate", "No se identificó el producto más rentable")

    def test_sell_product_success(self):
            
            product = Product(name="Helado de Chocolate", selling_price=5.0)
            ingredient = Ingredient(name="Leche", inventory=20)
            product.ingredients.append(ingredient)

            success, ingredientes_faltantes = sell_product(product)

            self.assertTrue(success)
            self.assertEqual(ingredientes_faltantes, [])

    def test_sell_product_no_inventory(self):
        """Prueba cuando un ingrediente no tiene inventario."""
        product = Product(name="Helado de Fresa", selling_price=5.0)
        ingredient = Ingredient(name="Fresas", inventory=0)
        product.ingredients.append(ingredient)

        success, ingredientes_faltantes = sell_product(product)

        self.assertFalse(success)
        self.assertIn("Fresas", ingredientes_faltantes)

    def test_sell_product_low_inventory(self):
        """Prueba cuando un ingrediente tiene menos de 10 en inventario."""
        product = Product(name="Helado de Vainilla", selling_price=5.0)
        ingredient = Ingredient(name="Vainilla", inventory=5)
        product.ingredients.append(ingredient)

        success, ingredientes_faltantes = sell_product(product)

        self.assertFalse(success)
        self.assertIn("No hay suficiente inventario de Vainilla para la venta", ingredientes_faltantes)

    def test_sell_product_multiple_ingredients_low_inventory(self):
        """Prueba cuando varios ingredientes tienen inventario bajo o agotado."""
        product = Product(name="Helado Mixto", selling_price=6.0)
        ingredient1 = Ingredient(name="Chocolate", inventory=8)
        ingredient2 = Ingredient(name="Leche", inventory=0)
        product.ingredients.extend([ingredient1, ingredient2])

        success, ingredientes_faltantes = sell_product(product)

        self.assertFalse(success)
        self.assertIn("No hay suficiente inventario de Chocolate para la venta", ingredientes_faltantes)
        self.assertIn("Leche", ingredientes_faltantes)

    def test_sell_product_no_product(self):
        """Prueba cuando el producto no existe."""
        success, ingredientes_faltantes = sell_product(None)

        self.assertFalse(success)
        self.assertEqual(ingredientes_faltantes, [])