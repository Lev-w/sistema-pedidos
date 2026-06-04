import app.database.db as db

def crear_producto(nombre, descripcion, precio, stock):
    producto_id = db.crear_producto(nombre, descripcion, precio, stock)
    return {
        "id": producto_id,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "stock": stock
    }

def obtener_productos(nombre, page, limit, orden):
    offset = (page - 1) * limit

    productos = db.obtener_productos(nombre, limit, offset, orden)

    total = db.total_registros_productos()

    total_pages = (total + limit - 1) // limit
    
    return {
        "productos": productos,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    }

def obtener_producto_por_id(producto_id):
    return db.obtener_producto_por_id(producto_id)

def actualizar_producto(nombre, descripcion, precio, stock, producto_id):
    actualizado = db.actualizar_producto_por_id(nombre, descripcion, precio, stock, producto_id)

    if not actualizado:
        return None

    return db.obtener_producto_por_id(producto_id)

def eliminar_producto(producto_id):
    return db.eliminar_producto(producto_id)