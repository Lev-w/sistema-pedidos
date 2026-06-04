from flask import request, jsonify, Blueprint, abort
import app.validators.usuario_validators as usuario_validators
import app.services.usuario_service as usuario_services
import app.utils.responses as responses
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.utils.decorators import roles_required

usuario_bp = Blueprint("usuario_bp", __name__, url_prefix="/usuarios")

@usuario_bp.route("", methods=["POST"])
def crear_usuario():
    data = request.get_json()
    datos, error = usuario_validators.validar_crear_usuario(data)

    if error:
        abort(400, description=error)
    
    nuevo_usuario = usuario_services.crear_usuario(datos["nombre"], datos["correo"], datos["password"])

    if not nuevo_usuario:
        abort(400, description="El correo ya está registrado")

    return jsonify(responses.success_response(data=nuevo_usuario, mensaje="Usuario creado exitosamente")), 201

@usuario_bp.route("/<int:usuario_id>", methods=["GET"])
@jwt_required()
def obtener_usuario(usuario_id):
    usuario = usuario_services.obtener_usuario_por_id(usuario_id)

    if not usuario:
        abort(404, description="Usuario no encontrado")

    return jsonify(responses.success_response(data=usuario)), 200

@usuario_bp.route("/<int:usuario_id>", methods=["DELETE"])
@jwt_required()
@roles_required("admin")
def eliminar_usuario(usuario_id):
    usuario = usuario_services.obtener_usuario_por_id(usuario_id)

    if not usuario:
        abort(404, description="Usuario no encontrado")

    usuario_autenticado = int(get_jwt_identity())

    if usuario_autenticado == usuario_id:
        abort(403, description="No puedes eliminarte a ti mismo")

    eliminado = usuario_services.eliminar_usuario(usuario_id)

    if not eliminado:
        abort(500, description="Error al eliminar usuario")

    return jsonify(responses.success_response(mensaje="Usuario eliminado exitosamente")), 200

@usuario_bp.route("", methods=["GET"])
@jwt_required()
@roles_required("admin")
def obtener_usuarios():
    nombre = str(request.args.get("nombre", ""))
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    orden= request.args.get("orden", None)

    usuarios = usuario_services.obtener_usuarios(nombre, page, limit, orden)

    return jsonify(
        responses.success_response(
            data=usuarios["usuarios"],
            mensaje="Usuarios obtenidos",
            meta=usuarios["meta"]
        )
    )

@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    datos, error = usuario_validators.validar_login(data)

    if error:
        abort(400, description=error)

    usuario = usuario_services.login(datos["correo"], datos["password"])

    if not usuario:
        abort(401, description="Credenciales inválidas")

    token = create_access_token(identity=str(usuario["id"]))

    return jsonify(responses.success_response(data={"token": token, "usuario": usuario}, mensaje="Login exitoso")), 200

@usuario_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    usuario_id = int(get_jwt_identity())

    usuario = usuario_services.obtener_usuario_por_id(usuario_id)

    if not usuario:
        abort(404, description="Usuario no encontrado")

    return jsonify(
        responses.success_response(
            data=usuario,
            mensaje="Perfil obtenido"
        )
    ), 200