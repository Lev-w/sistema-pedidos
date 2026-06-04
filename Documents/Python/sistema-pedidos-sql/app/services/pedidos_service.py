import app.database.db as db

def crear_pedido(usuario_id, productos):
    con = db.conectar()

    try:
        total = 0
        detalles = []

        estado = db.obtener_estado_por_nombre(con, "pendiente")

        if not estado:
            return None
        
        estado_id = estado["id"]

        for item in productos:
            producto_id = item["producto_id"]
            cantidad = item["cantidad"]

            producto = db.obtener_producto_por_id_conexion(con, producto_id)

            if not producto:
                con.rollback()
                return None

            if producto["stock"] < cantidad:
                con.rollback()
                return None

            subtotal = producto["precio"] * cantidad

            total += subtotal

            detalles.append({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio_unitario": producto["precio"],
                "subtotal": subtotal
            })

        pedido_id = db.crear_pedido(con, usuario_id, estado_id, total)

        detalles_finales = []

        for detalle in detalles:
            detalles_finales.append((
                pedido_id,
                detalle["producto_id"],
                detalle["cantidad"],
                detalle["precio_unitario"],
                detalle["subtotal"]
            ))

        db.crear_detalles_pedido(con, detalles_finales)

        for detalle in detalles:
            db.actualizar_stock(con, detalle["producto_id"], detalle["cantidad"])

                
        con.commit()
            
        return {
            "pedido_id": pedido_id,
            "total": total
        }
        
    except Exception as e:
        print(e)
        con.rollback()
        return None
    
    finally:
        con.close()

def obtener_pedido_por_id(pedido_id):
    pedido = db.obtener_pedido_por_id(pedido_id)

    if not pedido:
        return None
    
    detalles = db.obtener_detalles_pedido(pedido_id)

    pedido["productos"] = detalles

    return pedido

def obtener_pedidos(nombre, page, limit, orden):
    offset = (page - 1) * limit

    pedidos = db.obtener_pedidos(nombre, limit, offset, orden)

    total = db.total_registros_pedidos()

    total_pages = (total + limit - 1) // limit

    return {
        "pedidos": pedidos,
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages
        }
    }

def obtener_pedidos_por_usuario(usuario_id):
    pedidos = db.obtener_pedidos_usuario(usuario_id)

    for pedido in pedidos:

        detalles = db.obtener_detalles_pedido(
            pedido["id"]
        )

        pedido["productos"] = detalles

    return pedidos

def actualizar_estado_pedido(pedido_id, nuevo_estado_nombre):
    con = db.conectar()
    pedido = db.obtener_pedido_por_id(pedido_id)

    if not pedido:
        return None, "Pedido no encontrado"
                
    estado_actual = pedido["estado"]

    if estado_actual == "cancelado":
        return False, "El pedido ya está cancelado"
                
    if estado_actual == "entregado":
        return False, "El pedido ya está entregado"

    nuevo_estado = db.obtener_estado_por_nombre(con, nuevo_estado_nombre)

    if not nuevo_estado:
        return False, "El nuevo estado no es válido"

    actualizado = db.actualizar_estado_pedido(pedido_id, nuevo_estado["id"])

    if actualizado:
        return db.obtener_pedido_por_id(pedido_id), None

    return False, "Error al actualizar el estado del pedido"

def cancelar_pedido(usuario_id, pedido_id):
    con = db.conectar()
    try:
        pedido = db.obtener_pedido_por_id(pedido_id)

        if not pedido:
            return False, "Pedido no encontrado"

        if pedido["usuario_id"] != usuario_id:
            return False, "No tienes permiso para cancelar este pedido"

        if pedido["estado"] == "cancelado":
            return False, "El pedido ya está cancelado"

        if pedido["estado"] == "entregado":
            return False, "El pedido ya está entregado"
        
        nuevo_estado = db.obtener_estado_por_nombre(con, "cancelado")

        if not nuevo_estado:
            return False, "Error al obtener el estado cancelado"

        actualizado = db.actualizar_estado_pedido(pedido_id, nuevo_estado["id"])

        if actualizado:
            detalles = db.obtener_detalles_pedido(pedido_id)
            for detalle in detalles:
                db.sumar_stock(con, detalle["producto_id"], detalle["cantidad"])
            con.commit()
            return True, None

    except Exception as e:
        print(e)
        con.rollback()
        return False, "Error al cancelar el pedido"
    
    finally:
        con.close()