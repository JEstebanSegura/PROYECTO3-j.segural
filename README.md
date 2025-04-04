# Documentación de API para Productos e Ingredientes

## API de Productos

### Rutas

#### `GET /api/products/`
Obtiene todos los productos disponibles en la base de datos.

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Helado de Chocolate",
    "selling_price": 5.99,
    "product_type": "Postre"
  },
  ...
]
```

#### `GET /api/products/<int:product_id>`
Obtiene un producto por su ID.

**Respuesta:**
```json
{
  "id": 1,
  "name": "Helado de Chocolate",
  "selling_price": 5.99,
  "product_type": "Postre"
}
```

#### `GET /api/products/name/<string:product_name>`
Obtiene un producto por su nombre.

**Respuesta:**
```json
{
  "id": 1,
  "name": "Helado de Chocolate",
  "selling_price": 5.99,
  "product_type": "Postre"
}
```

#### `GET /api/products/calories/<int:product_id>`
Obtiene las calorías totales de un producto.

**Respuesta:**
```json
{
  "product_id": 1,
  "name": "Helado de Chocolate",
  "calories": 250
}
```

#### `GET /api/products/profit/<int:product_id>`
Obtiene la ganancia de un producto.

**Respuesta:**
```json
{
  "product_id": 1,
  "name": "Helado de Chocolate",
  "profit": 2.50
}
```

#### `GET /api/products/cost/<int:product_id>`
Obtiene el costo total de un producto.

**Respuesta:**
```json
{
  "product_id": 1,
  "name": "Helado de Chocolate",
  "cost": 3.49
}
```

#### `POST /api/products/sell/<int:product_id>`
Vende un producto y actualiza el inventario de ingredientes.

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Venta exitosa",
  "product": {
    "id": 1,
    "name": "Helado de Chocolate",
    "selling_price": 5.99
  }
}
```

**Respuesta con error:**
```json
{
  "success": false,
  "message": "No se pudo completar la venta",
  "missing_ingredients": ["Leche", "Chocolate"]
}
```

---

## API de Ingredientes

### Rutas

#### `GET /api/ingredients/`
Obtiene todos los ingredientes disponibles.

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Leche",
    "inventory": 50
  },
  ...
]
```

#### `GET /api/ingredients/<int:ingredient_id>`
Obtiene un ingrediente por su ID.

**Respuesta:**
```json
{
  "id": 1,
  "name": "Leche",
  "inventory": 50
}
```

#### `GET /api/ingredients/name/<string:ingredient_name>`
Obtiene un ingrediente por su nombre.

**Respuesta:**
```json
{
  "id": 1,
  "name": "Leche",
  "inventory": 50
}
```

#### `GET /api/ingredients/healthy/<int:ingredient_id>`
Determina si un ingrediente es saludable.

**Respuesta:**
```json
{
  "ingredient_id": 1,
  "name": "Leche",
  "is_healthy": true
}
```

#### `PATCH /api/ingredients/supply/<int:ingredient_id>`
Reabastece un ingrediente.

**Respuesta:**
```json
{
  "ingredient_id": 1,
  "name": "Leche",
  "new_inventory": 100
}
```

#### `POST /api/ingredients/<int:id>/suply`
Reabastece un ingrediente con autenticación de usuario.

**Requiere autenticación:** Sólo los usuarios con roles `admin` o `empleado` pueden ejecutar esta acción.

**Respuesta exitosa:**
```json
{
  "ingredient_id": 1,
  "name": "Leche",
  "new_inventory": 100
}
```

**Acceso denegado:**
```html
<p>Acceso denegado</p>
```

# PROYECTO3-j.segural
