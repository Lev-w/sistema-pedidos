import app.database.db as db
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

def crear_usuario(nombre, correo, password):

    usuario_existente = db.obtener_usuario_por_correo(correo)

    if usuario_existente:
        return None

    password_hash = generate_password_hash(password)

    usuario_id = db.crear_usuario(
        nombre,
        correo,
        password_hash
    )

    return {
        "id": usuario_id,
        "nombre": nombre,
        "correo": correo
    }

def obtener_usuarios(nombre, page, limit, orden):
    offset = (page - 1) * limit
    usuarios = db.obtener_usuarios(nombre, limit, offset, orden)
    total = db.total_registros_usuarios()
    total_pages = (total + limit - 1) // limit

    return {
        "usuarios": usuarios,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages
        }
    }

def obtener_usuario_por_id(usuario_id):
    return db.obtener_usuario_por_id(usuario_id)

def eliminar_usuario(usuario_id):
    return db.eliminar_usuario(usuario_id)

def login(correo, password):
    usuario = db.obtener_usuario_por_correo(correo)
    if usuario and check_password_hash(usuario['password'], password):
        usuario.pop('password', None) # Eliminar la contraseña del diccionario antes de devolverlo
        return usuario
    return None