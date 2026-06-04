from flask import request, jsonify, Blueprint, abort
import app.services.producto_service as producto_service
import app.utils.responses as responses
from flask_jwt_extended import jwt_required
from app.utils.decorators import roles_required
import app.validators.producto_validators as producto_validators

producto_bp = Blueprint("producto_bp", __name__, url_prefix="/productos")

@producto_bp.route("", methods=["POST"])
@jwt_required()
@roles_required("admin")
def crear_producto():
    data = request.get_json()
    datos, error = producto_validators.validar_crear_producto(data)

    if error:
        abort(400, description=error)

    nuevo_producto = producto_service.crear_producto(datos["nombre"], datos["descripcion"], datos["precio"], datos["stock"])

    if not nuevo_producto:
        abort(500, description="Error al crear producto")

    return jsonify(responses.success_response(data=nuevo_producto, mensaje="Producto creado exitosamente")), 201

@producto_bp.route("", methods=["GET"])
@jwt_required()
def obtener_productos():
    data = request.args.to_dict()

    datos, error = producto_validators.validar_get(data)

    if error:
        abort(400, description=error)

    productos = producto_service.obtener_productos(datos["nombre"], datos["page"], datos["limit"], datos["orden"])

    return jsonify(responses.success_response(data=productos["productos"], mensaje="Productos obtenidos exitosamente", meta=productos["meta"])), 200

@producto_bp.route("/<int:producto_id>", methods=["GET"])
@jwt_required()
def obtener_producto(producto_id):
    producto = producto_service.obtener_producto_por_id(producto_id)

    if not producto:
        abort(404, description="Producto no encontrado")

    return jsonify(responses.success_response(data=producto, mensaje="Producto obtenido exitosamente")), 200

@producto_bp.route("/<int:producto_id>", methods=["PUT"])
@jwt_required()
@roles_required("admin")
def actualizar_producto(producto_id):
    data = request.get_json()
    datos, error = producto_validators.validar_actualizar_producto(data)

    if error:
        abort(400, description=error)

    producto_actualizado = producto_service.actualizar_producto(datos["nombre"], datos["descripcion"], datos["precio"], datos["stock"], producto_id)

    if not producto_actualizado:
        abort(404, description="Producto no encontrado")

    return jsonify(responses.success_response(data=producto_actualizado, mensaje="Producto actualizado exitosamente")), 200

@producto_bp.route("/<int:producto_id>", methods=["DELETE"])
@jwt_required()
@roles_required("admin")
def eliminar_producto(producto_id):
    producto = producto_service.obtener_producto_por_id(producto_id)

    if not producto:
        abort(404, description="Producto no encontrado")

    producto_eliminado = producto_service.eliminar_producto(producto_id)

    if not producto_eliminado:
        abort(500, description="Error al eliminar producto")

    return jsonify(responses.success_response(mensaje="Producto eliminado exitosamente")), 200