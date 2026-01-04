"""
Rutas de la API para gestión de cabañas.
"""
from flask import Blueprint, request
from app.services import get_cabin_service
from app.utils.responses import success_response, error_response, not_found_response

cabins_bp = Blueprint('cabins', __name__)
cabin_service = get_cabin_service()


@cabins_bp.route('', methods=['GET'])
def get_all_cabins():
    """
    GET /api/cabins
    Obtiene todas las cabañas del complejo.
    
    Returns:
        JSON con la lista de cabañas
    """
    cabins = cabin_service.get_all()
    cabins_data = [cabin.to_dict() for cabin in cabins]
    
    return success_response(cabins_data, message=f"Se encontraron {len(cabins_data)} cabañas")


@cabins_bp.route('/<int:cabin_id>', methods=['GET'])
def get_cabin(cabin_id):
    """
    GET /api/cabins/<id>
    Obtiene una cabaña específica por ID.
    
    Args:
        cabin_id: ID de la cabaña
        
    Returns:
        JSON con los datos de la cabaña
    """
    cabin = cabin_service.get_by_id(cabin_id)
    
    if not cabin:
        return not_found_response("Cabaña", cabin_id)
    
    return success_response(cabin.to_dict())


@cabins_bp.route('/pair/<int:pair_group>', methods=['GET'])
def get_cabins_by_pair(pair_group):
    """
    GET /api/cabins/pair/<pair_group>
    Obtiene las cabañas de un grupo de par específico.
    
    Args:
        pair_group: Número del grupo de par (1-8)
        
    Returns:
        JSON con la lista de cabañas del par
    """
    if pair_group < 1 or pair_group > 8:
        return error_response("El grupo de par debe estar entre 1 y 8")
    
    cabins = cabin_service.get_by_pair_group(pair_group)
    cabins_data = [cabin.to_dict() for cabin in cabins]
    
    return success_response(
        cabins_data,
        message=f"Se encontraron {len(cabins_data)} cabañas en el par {pair_group}"
    )


@cabins_bp.route('/<int:cabin_id>', methods=['PUT'])
def update_cabin(cabin_id):
    """
    PUT /api/cabins/<id>
    Actualiza los datos de una cabaña.
    
    Args:
        cabin_id: ID de la cabaña
        
    Body:
        JSON con los campos a actualizar (name, capacity, amenities)
        
    Returns:
        JSON con la cabaña actualizada
    """
    if not request.json:
        return error_response("Se requiere un body JSON")
    
    cabin = cabin_service.get_by_id(cabin_id)
    if not cabin:
        return not_found_response("Cabaña", cabin_id)
    
    updated_cabin = cabin_service.update(cabin_id, request.json)
    
    return success_response(
        updated_cabin.to_dict(),
        message="Cabaña actualizada exitosamente"
    )
