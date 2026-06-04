def validar_crear_producto(data):
    if not data:
        return None, "No se proporcionaron datos."
    
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    precio = data.get("precio")
    stock = data.get("stock")

    if not isinstance(nombre, str) or not nombre.strip():
        return None, "El nombre del producto debe ser una cadena de texto."
    
    if descripcion is not None and not isinstance(descripcion, str):
        return None, "La descripción del producto debe ser una cadena de texto."

    if not isinstance(precio, (int, float)) or precio < 0:
        return None, "El precio del producto es obligatorio y debe ser un número positivo."

    if not isinstance(stock, int) or stock < 0:
        return None, "El stock del producto es obligatorio y debe ser un número entero positivo."

    return {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock
    }, None

def validar_actualizar_producto(data):
    if not data:
        return None, "No se proporcionaron datos."
    
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    precio = data.get("precio")
    stock = data.get("stock")

    if not nombre and not isinstance(nombre, str):
        return None, "El nombre del producto debe ser una cadena de texto."
    
    if descripcion is not None and not isinstance(descripcion, str):
        return None, "La descripción del producto debe ser una cadena de texto."

    try:
        precio = float(precio)
    except (TypeError, ValueError):
        return None, "El precio del producto debe ser un número."

    try:
        precio = int(precio)
    except (TypeError, ValueError):
        return None, "El precio del producto debe ser un número entero."
    
    if all(valor is None for valor in [nombre, descripcion, precio, stock]):
        return None, "Al menos un campo debe ser proporcionado para actualizar."

    return {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock
    }, None

def validar_get(data):
    if not data:
        data = {}

    nombre = data.get("nombre")
    page = data.get("page")
    limit = data.get("limit")
    orden = data.get("orden")

    try:
        nombre = str(nombre) if nombre else None
        nombre = nombre.strip() if nombre else None
    except ValueError:
        return None, "El parámetro 'nombre' debe ser una cadena de texto"

    try:
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
        if page < 1 or limit < 1:
            return None, "Los parámetros 'page' y 'limit' deben ser enteros positivos"
    except ValueError:
        return None, "Los parámetros 'page' y 'limit' deben ser enteros"
    
    datos_limpios = {
        "nombre": nombre,
        "page": page,
        "limit": limit,
        "orden": orden
    }
    return datos_limpios, None