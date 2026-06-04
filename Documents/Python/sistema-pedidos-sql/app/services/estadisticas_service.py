import app.database.db as db


def obtener_ventas():
    ventas_totales = db.ventas_totales_pedidos()

    productos_mas_vendidos = (
        db.obtener_productos_mas_vendidos()
    )

    usuarios_mas_compradores = (
        db.usuarios_mas_compras()
    )

    return {
        "ventas_totales": ventas_totales,
        "productos_mas_vendidos": productos_mas_vendidos,
        "usuarios_mas_compradores": usuarios_mas_compradores
    }