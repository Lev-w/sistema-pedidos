from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity
import app.services.usuario_service as usuario_service

def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario_id = int(get_jwt_identity())

            usuario = usuario_service.obtener_usuario_por_id(usuario_id)

            if not usuario:
                abort(404, description="Usuario no encontrado")

            if usuario["rol"] not in roles:
                abort(403, description="No tienes permisos")

            return func(*args, **kwargs)
        return wrapper
    return decorator