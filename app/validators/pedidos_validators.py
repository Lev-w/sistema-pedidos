def validar_crear_pedido(data):
    if not data:
        return None, "No se proporcionaron datos."

    productos = data.get("productos")

    if productos is None:
        return None, "Se requiere la lista de productos."

    if not isinstance(productos, list):
        return None, "Productos debe ser una lista."

    if len(productos) ==  0:
        return None, "El pedido debe contener al menos un producto."

    productos_limpios = []

    for item in productos:

        if not isinstance(item, dict):
            return None, "Cada producto debe ser un objeto."

        producto_id = item.get("producto_id")
        cantidad = item.get("cantidad")

        if not isinstance(producto_id, int) or producto_id <= 0:
            return None, "Producto_id inválido."

        if not isinstance(cantidad, int) or cantidad <= 0:
            return None, "Cantidad inválida."

        productos_limpios.append({
            "producto_id": producto_id,
            "cantidad": cantidad
        })

    return {
        "productos": productos_limpios
    }, None

def validar_estado_pedido(data):
    estados_validos = [
        "pendiente",
        "enviado",
        "entregado",
        "cancelado"
    ]
    
    if not data:
        return None, "No se enviaron datos"

    estado = data.get("estado")

    if not estado:
        return None, "El estado es requerido"

    if estado not in estados_validos:
        return None, "Estado inválido"

    return {
        "estado": estado
    }, None