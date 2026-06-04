from flask import request, jsonify, Blueprint, abort
import app.utils.responses as responses
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import roles_required
import app.services.pedidos_service as pedidos_service
import app.validators.pedidos_validators as pedidos_validators

pedidos_bp = Blueprint("pedidos_bp", __name__, url_prefix="/pedidos")

@pedidos_bp.route("", methods=["POST"])
@jwt_required()
def crear_pedido():
    data = request.get_json()

    datos, error = pedidos_validators.validar_crear_pedido(data)

    if error:
        abort(400, description=error)

    usuario_id = int(get_jwt_identity())
    pedido = pedidos_service.crear_pedido(usuario_id, datos["productos"])

    if not pedido:
        abort(400, description="Error al crear el pedido")

    return jsonify(responses.success_response(data=pedido, mensaje="Pedido creado exitosamente")), 201

@pedidos_bp.route("/<int:pedido_id>", methods=["GET"])
@jwt_required()
@roles_required("admin")
def obtener_pedido(pedido_id):
    pedido = pedidos_service.obtener_pedido_por_id(pedido_id)

    if not pedido:
        abort(404, description="Pedido no encontrado")

    return jsonify(responses.success_response(data=pedido))

@pedidos_bp.route("", methods=["GET"])
@jwt_required()
@roles_required("admin")
def obtener_pedidos():
    nombre = str(request.args.get("nombre", ""))
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    orden = request.args.get("orden", None)

    pedidos = pedidos_service.obtener_pedidos(nombre, page, limit, orden)

    return jsonify(responses.success_response(data=pedidos["pedidos"], mensaje="Pedidos obtenidos exitosamente", meta=pedidos["meta"])), 200

@pedidos_bp.route("/mis-pedidos", methods=["GET"])
@jwt_required()
def obtener_mis_pedidos():
    usuario_id = int(get_jwt_identity())

    pedidos = pedidos_service.obtener_pedidos_por_usuario(usuario_id)

    return jsonify(responses.success_response(data=pedidos, mensaje="Pedidos obtenidos exitosamente")), 200

@pedidos_bp.route("/<int:pedido_id>/estado", methods=["PUT"])
@jwt_required()
@roles_required("admin")
def actualizar_estado_pedido(pedido_id):
    data = request.get_json()

    datos, error = pedidos_validators.validar_estado_pedido(data)

    if error:
        abort(400, description=error)

    pedido, error = pedidos_service.actualizar_estado_pedido(pedido_id, datos["estado"])

    if error:
        abort(404, description=error)

    return jsonify(responses.success_response(data=pedido, mensaje="Estado del pedido actualizado exitosamente")), 200

@pedidos_bp.route("/<int:pedido_id>/cancelar", methods=["PUT"])
@jwt_required()
def cancelar_pedido(pedido_id):
    usuario_id = int(get_jwt_identity())

    cancelado, error = pedidos_service.cancelar_pedido(usuario_id, pedido_id)

    if error:
        abort(404, description=error)

    return jsonify(responses.success_response(mensaje="Pedido cancelado exitosamente")), 200