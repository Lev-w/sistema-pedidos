import sqlite3

DB_NAME = "tienda.db"

def conectar():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

#---------------------------TABLAS----------------------------------

def crear_tabla_usuarios():
    with conectar() as con:
        con.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'cliente' CHECK(rol IN ('admin', 'cliente', 'vendedor')),
            activo BOOLEAN NOT NULL DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    )
        
def crear_tabla_productos():
    with conectar() as con:
        con.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL CHECK(precio >= 0),
            stock INTEGER NOT NULL CHECK(stock >= 0),
            activo BOOLEAN NOT NULL DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
    )
        
def crear_tabla_estados_pedido():
    with conectar() as con:
        con.execute('''
        CREATE TABLE IF NOT EXISTS estados_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )'''
    )
        
def crear_tabla_pedidos():
    with conectar() as con:
        con.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            estado_id INTEGER NOT NULL,
            total REAL NOT NULL CHECK(total >= 0),
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY (estado_id) REFERENCES estados_pedido(id)
        )'''
    )
        
def crear_tabla_detalles_pedido():
    with conectar() as con:
        con.execute('''
        CREATE TABLE IF NOT EXISTS detalles_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL CHECK(cantidad > 0),
            precio_unitario REAL NOT NULL CHECK(precio_unitario >= 0),
            subtotal REAL NOT NULL CHECK(subtotal >= 0),

            FOREIGN KEY (pedido_id)
                REFERENCES pedidos(id)
                ON DELETE CASCADE,

            FOREIGN KEY (producto_id)
                REFERENCES productos(id)
        )'''
    )
        
def insertar_estados():
    estados = [
        ("pendiente",),
        ("pagado",),
        ("enviado",),
        ("entregado",),
        ("cancelado",)
    ]

    with conectar() as con:
        con.executemany('''
        INSERT OR IGNORE INTO estados_pedido (nombre)
        VALUES (?)
        ''', estados)

def crear_tablas():
    crear_tabla_usuarios()
    crear_tabla_productos()
    crear_tabla_estados_pedido()
    crear_tabla_pedidos()
    crear_tabla_detalles_pedido()
    insertar_estados()

#---------------------------USUARIOS----------------------------------

def crear_usuario(nombre, correo, password):
    with conectar() as con:
        cursor = con.execute('''
        INSERT INTO usuarios (nombre, correo, password)
        VALUES (?, ?, ?)
        ''', (nombre, correo, password))
        return cursor.lastrowid

def obtener_usuarios(nombre, limit, offset, orden):
    with conectar() as con:
        query = 'SELECT id, nombre, correo, rol, fecha_creacion FROM usuarios WHERE activo = 1'
        params = []

        if nombre:
            query += ' AND nombre LIKE ?'
            params.append(f'%{nombre}%')

        if orden:
            orden_options = {
                "fecha_asc": "fecha_creacion ASC",
                "fecha_desc": "fecha_creacion DESC",
                "nombre_asc": "nombre ASC",
                "nombre_desc": "nombre DESC"
            }
            if orden in orden_options:
                query += f' ORDER BY {orden_options[orden]}'

        query += ' LIMIT ? OFFSET ?'
        params.extend([limit, offset])

        cursor = con.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
def obtener_usuario_por_id(usuario_id):
    with conectar() as con:
        cursor = con.execute('SELECT id, nombre, correo, rol, fecha_creacion FROM usuarios WHERE id = ? AND activo = 1', (usuario_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
def eliminar_usuario(usuario_id):
    with conectar() as con:
        cursor = con.execute('UPDATE usuarios SET activo = 0 WHERE id = ?', (usuario_id,))
        return cursor.rowcount > 0

def obtener_usuario_por_correo(correo):
    with conectar() as con:
        cursor = con.execute('''
        SELECT * FROM usuarios
        WHERE correo = ?
        ''', (correo,))

        row = cursor.fetchone()
        return dict(row) if row else None
    

#---------------------------PRODUCTOS----------------------------------
def crear_producto(nombre, descripcion, precio, stock):
    with conectar() as con:
        cursor = con.execute('''
        INSERT INTO productos (nombre, descripcion, precio, stock)
        VALUES (?, ?, ?, ?)
        ''', (nombre, descripcion, precio, stock))
        return cursor.lastrowid
    
def obtener_productos(nombre, limit, offset, orden):
    with conectar() as con:
        query = 'SELECT id, nombre, descripcion, precio, stock, fecha_creacion FROM productos WHERE activo = 1'
        params = []

        if nombre:
            query += ' AND nombre LIKE ?'
            params.append(f'%{nombre}%')

        if orden:
            orden_options = {
                'fecha_desc': 'fecha_creacion DESC',
                'fecha_asc': 'fecha_creacion ASC',
                'precio_asc': 'precio ASC',
                'precio_desc': 'precio DESC',
                'stock_asc': 'stock ASC',
                'stock_desc': 'stock DESC',
            }
            if orden in orden_options:
                query += f' ORDER BY {orden_options[orden]}'

        query += ' LIMIT ? OFFSET ?'
        params.extend([limit, offset])

        cursor = con.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def obtener_producto_por_id(producto_id):
    with conectar() as con:
        cursor = con.execute('SELECT id, nombre, descripcion, precio, stock, fecha_creacion FROM productos WHERE id = ? AND activo = 1', (producto_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
def actualizar_producto_por_id(nombre, descripcion, precio, stock, producto_id):
    with conectar() as con:
        cursor = con.execute('''
        UPDATE productos
        SET nombre = ?, descripcion = ?, precio = ?, stock = ?
        WHERE id = ? AND activo = 1
        ''', (nombre, descripcion, precio, stock, producto_id))
        return cursor.rowcount > 0
    
def eliminar_producto(producto_id):
    with conectar() as con:
        cursor = con.execute('UPDATE productos SET activo = 0 WHERE id = ?', (producto_id,))
        return cursor.rowcount > 0
    
#---------------------------PEDIDOS----------------------------------
def crear_pedido(con, usuario_id, estado_id, total):
    cursor = con.execute('''
    INSERT INTO pedidos (usuario_id, estado_id, total)
    VALUES (?, ?, ?)
    ''', (usuario_id, estado_id, total))
    return cursor.lastrowid

def crear_detalles_pedido(con, detalles):
    con.executemany('''
        INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
        VALUES (?, ?, ?, ?, ?)
    ''', (detalles))

def actualizar_stock(con, producto_id, cantidad):
    con.execute('''
    UPDATE productos
    SET stock = stock - ?
    WHERE id = ?
    ''', (cantidad, producto_id))

def obtener_estado_por_nombre(con, nombre):
    cursor = con.execute('''
        SELECT * FROM estados_pedido WHERE nombre = ?
    ''', (nombre,))

    row = cursor.fetchone()
    return dict(row) if row else None

def obtener_producto_por_id_conexion(con, producto_id):

    cursor = con.execute(
        '''
        SELECT *
        FROM productos
        WHERE id = ?
        AND activo = 1
        ''',
        (producto_id,)
    )

    row = cursor.fetchone()

    return dict(row) if row else None

def obtener_pedido_por_id(pedido_id):
    with conectar() as con:
        cursor = con.execute('''
            SELECT p.id, p.total, p.fecha_creacion, u.id AS usuario_id, u.nombre AS usuario_nombre, u.correo, e.nombre AS estado
            FROM pedidos p JOIN usuarios u ON p.usuario_id = u.id
            JOIN estados_pedido e ON p.estado_id = e.id
            WHERE p.id = ?
            ''', (pedido_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
def obtener_detalles_pedido(pedido_id):
    with conectar() as con:
        cursor = con.execute('''
            SELECT dp.producto_id, pr.nombre, dp.cantidad, dp.precio_unitario, dp.subtotal
            FROM detalles_pedido dp JOIN productos pr ON dp.producto_id = pr.id
            WHERE dp.pedido_id = ?
            ''', (pedido_id,))
        return [dict(row) for row in cursor.fetchall()]
    
def obtener_pedidos(nombre, limit, offset, orden):
    with conectar() as con:
            query = '''
            SELECT p.id, p.total, p.fecha_creacion, u.nombre AS usuario_nombre, e.nombre AS estado
            FROM pedidos p JOIN usuarios u ON p.usuario_id = u.id
            JOIN estados_pedido e ON p.estado_id = e.id
            WHERE 1=1
            '''
            params = []

            if nombre:
                query += ' AND u.nombre LIKE ?'
                params.append(f'%{nombre}%')

            if orden:
                orden_options = {
                    "total_asc": "p.total ASC",
                    "total_desc": "p.total DESC",
                    "fecha_asc": "p.fecha_creacion ASC",
                    "fecha_desc": "p.fecha_creacion DESC"
                }
                if orden in orden_options:
                    query += f' ORDER BY {orden_options[orden]}'

            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])
            
            cursor = con.execute(query, tuple(params))
            return [dict(row) for row in cursor.fetchall()]

def obtener_pedidos_usuario(usuario_id):
    with conectar() as con:
        cursor = con.execute('''
            SELECT p.id, p.total, p.fecha_creacion, e.nombre AS estado
            FROM pedidos p JOIN estados_pedido e ON p.estado_id = e.id
            WHERE p.usuario_id = ?
            ORDER BY p.fecha_creacion DESC
            ''', (usuario_id,))
        return [dict(row) for row in cursor.fetchall()]

def actualizar_estado_pedido(pedido_id, estado_id):
    with conectar() as con:
        cursor = con.execute('''
            UPDATE pedidos
            SET estado_id = ?
            WHERE id = ?
            ''', (estado_id, pedido_id))
        return cursor.rowcount > 0

def sumar_stock(con, producto_id, cantidad):
    con.execute('''
    UPDATE productos
    SET stock = stock + ?
    WHERE id = ?
    ''', (cantidad, producto_id))

#-----------------------REGISTROS----------------------------------

def total_registros_pedidos():
    with conectar() as con:
        cursor = con.execute('SELECT COUNT(*) AS total FROM pedidos')
        row = cursor.fetchone()
        return row['total'] if row else 0
    
def total_registros_productos():
    with conectar() as con:
        cursor = con.execute('SELECT COUNT(*) AS total FROM productos WHERE activo = 1')
        row = cursor.fetchone()
        return row['total'] if row else 0
    
def total_registros_usuarios():
    with conectar() as con:
        cursor = con.execute('SELECT COUNT(*) AS total FROM usuarios WHERE activo = 1')
        row = cursor.fetchone()
        return row['total'] if row else 0

#-----------------------ESTADISTICAS----------------------------------------

def ventas_totales_pedidos():
    with conectar() as con:
        cursor = con.execute('''
            SELECT SUM(p.total) AS total_ventas
            FROM pedidos p
            JOIN estados_pedido e
            ON p.estado_id = e.id
            WHERE e.nombre != 'cancelado'
        ''')
        row = cursor.fetchone()
        return row['total_ventas'] or 0

def obtener_productos_mas_vendidos():
    with conectar() as con:
        cursor = con.execute("""
            SELECT
                pr.id,
                pr.nombre,
                SUM(dp.cantidad) AS cantidad_vendida
            FROM detalles_pedido dp
            JOIN productos pr
                ON dp.producto_id = pr.id
            GROUP BY pr.id, pr.nombre
            ORDER BY cantidad_vendida DESC
            LIMIT 5
        """)

        return [dict(row) for row in cursor.fetchall()]

def usuarios_mas_compras():
    with conectar() as con:
        cursor = con.execute("""
            SELECT
                u.id,
                u.nombre,
                COUNT(p.id) AS cantidad_pedidos,
                SUM(p.total) AS total_gastado
            FROM usuarios u
            JOIN pedidos p
                ON p.usuario_id = u.id
            JOIN estados_pedido e
                ON p.estado_id = e.id
            WHERE e.nombre != 'cancelado'
            GROUP BY u.id, u.nombre
            ORDER BY total_gastado DESC
            LIMIT 5
        """)

        return [dict(row) for row in cursor.fetchall()]
