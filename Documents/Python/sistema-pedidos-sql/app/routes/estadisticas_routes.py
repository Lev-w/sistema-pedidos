import app.services.estadisticas_service as estadisticas_service
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import roles_required
import app.utils.responses as responses


estadisticas_bp = Blueprint('estadisticas', __name__, url_prefix='/estadisticas')

@estadisticas_bp.route('', methods=['GET'])
@jwt_required()
@roles_required('admin')
def obtener_estadisticas_ventas():
    estadisticas = estadisticas_service.obtener_ventas()
    return jsonify(responses.success_response(data=estadisticas, mensaje="Estadísticas de ventas obtenidas exitosamente")), 200