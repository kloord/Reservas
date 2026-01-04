"""
Rutas de la API para consultar disponibilidad de cabañas.
"""
from flask import Blueprint, request
from app.services import get_cabin_service, get_reservation_service
from app.utils.responses import success_response, error_response
from app.utils.validators import parse_date, validate_date_range

availability_bp = Blueprint('availability', __name__)
cabin_service = get_cabin_service()
reservation_service = get_reservation_service()


@availability_bp.route('', methods=['GET'])
def check_availability():
    """
    GET /api/availability
    Consulta la disponibilidad de cabañas en un rango de fechas.
    
    Query params requeridos:
        - start_date: Fecha de inicio (YYYY-MM-DD)
        - end_date: Fecha de término (YYYY-MM-DD)
    
    Query params opcionales:
        - cabin_id: Consultar disponibilidad de una cabaña específica
    
    Returns:
        JSON con información de disponibilidad de cabañas
    """
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    cabin_id = request.args.get('cabin_id', type=int)
    
    # Validar que se proporcionaron las fechas
    if not start_date_str or not end_date_str:
        return error_response("Se requieren los parámetros 'start_date' y 'end_date'")
    
    # Parsear fechas
    start_date, error = parse_date(start_date_str)
    if error:
        return error_response(error)
    
    end_date, error = parse_date(end_date_str)
    if error:
        return error_response(error)
    
    # Validar rango de fechas
    validation_error = validate_date_range(start_date, end_date)
    if validation_error:
        return error_response(validation_error)
    
    # Si se especificó una cabaña, consultar solo esa
    if cabin_id:
        cabin = cabin_service.get_by_id(cabin_id)
        if not cabin:
            return error_response(f"La cabaña con ID {cabin_id} no existe")
        
        is_available = reservation_service.check_availability(cabin_id, start_date, end_date)
        
        result = {
            'cabin': cabin.to_dict(),
            'is_available': is_available,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        
        # Si no está disponible, incluir las reservas conflictivas
        if not is_available:
            conflicting_reservations = [
                r.to_dict() for r in reservation_service.get_by_cabin(cabin_id)
                if r.overlaps_with_range(start_date, end_date)
            ]
            result['conflicting_reservations'] = conflicting_reservations
        
        return success_response(result)
    
    # Consultar disponibilidad de todas las cabañas
    all_cabins = cabin_service.get_all()
    available_cabin_ids = reservation_service.get_available_cabins(start_date, end_date)
    
    # Obtener reservas del rango para cabañas ocupadas
    reservations_in_range = reservation_service.get_by_date_range(start_date, end_date)
    
    # Construir respuesta detallada
    cabins_status = []
    for cabin in all_cabins:
        is_available = cabin.id in available_cabin_ids
        
        cabin_data = {
            'cabin': cabin.to_dict(),
            'is_available': is_available
        }
        
        # Si no está disponible, incluir la reserva activa
        if not is_available:
            active_reservation = next(
                (r for r in reservations_in_range if r.cabin_id == cabin.id),
                None
            )
            if active_reservation:
                cabin_data['current_reservation'] = active_reservation.to_dict()
        
        cabins_status.append(cabin_data)
    
    result = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'total_cabins': len(all_cabins),
        'available_count': len(available_cabin_ids),
        'occupied_count': len(all_cabins) - len(available_cabin_ids),
        'cabins': cabins_status
    }
    
    return success_response(
        result,
        message=f"{len(available_cabin_ids)} de {len(all_cabins)} cabañas disponibles"
    )


@availability_bp.route('/summary', methods=['GET'])
def get_availability_summary():
    """
    GET /api/availability/summary
    Obtiene un resumen rápido de disponibilidad.
    
    Query params requeridos:
        - start_date: Fecha de inicio (YYYY-MM-DD)
        - end_date: Fecha de término (YYYY-MM-DD)
    
    Returns:
        JSON con resumen de disponibilidad (solo IDs y contadores)
    """
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    if not start_date_str or not end_date_str:
        return error_response("Se requieren los parámetros 'start_date' y 'end_date'")
    
    # Parsear fechas
    start_date, error = parse_date(start_date_str)
    if error:
        return error_response(error)
    
    end_date, error = parse_date(end_date_str)
    if error:
        return error_response(error)
    
    # Validar rango
    validation_error = validate_date_range(start_date, end_date)
    if validation_error:
        return error_response(validation_error)
    
    # Obtener disponibilidad
    all_cabins = cabin_service.get_all()
    available_cabin_ids = reservation_service.get_available_cabins(start_date, end_date)
    occupied_cabin_ids = [c.id for c in all_cabins if c.id not in available_cabin_ids]
    
    result = {
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'available_cabin_ids': available_cabin_ids,
        'occupied_cabin_ids': occupied_cabin_ids,
        'available_count': len(available_cabin_ids),
        'occupied_count': len(occupied_cabin_ids),
        'total_count': len(all_cabins)
    }
    
    return success_response(result)
