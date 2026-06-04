import re

def correo_valido(correo):
    patron = r'^[^@]+@[^@]+\.[^@]+$'
    return re.match(patron, correo)

def validar_crear_usuario(data):
    if not data:
        return None, "Se requiere JSON."
    
    nombre = data.get("nombre")
    correo = data.get("correo")
    password = data.get("password")

    if not nombre or not nombre.strip():
        return None, "Se requiere un nombre."

    if len(nombre.strip()) < 2:
        return None, "El nombre debe tener al menos 2 caracteres."

    if not correo or not correo.strip():
        return None, "Se requiere un correo."

    if not correo_valido(correo.strip().lower()):
        return None, "El correo no es válido."

    if not password or not password.strip():
        return None, "Se requiere una contraseña."
    
    nombre = nombre.strip().lower()
    correo = correo.strip().lower()
    password = password.strip()

    datos_limpios = {
        "nombre": nombre,
        "correo": correo,
        "password": password
    }

    return datos_limpios, None

def validar_login(data):
    if not data:
        return None, "Se requiere JSON."
    
    correo = data.get("correo")
    password = data.get("password")

    if not correo or not correo.strip():
        return None, "Se requiere un correo."

    if not password or not password.strip():
        return None, "Se requiere una contraseña."
    
    correo = correo.strip().lower()
    password = password.strip()

    datos_limpios = {
        "correo": correo,
        "password": password
    }

    return datos_limpios, None