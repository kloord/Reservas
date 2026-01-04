"""
Rutas de la API para gestión de reservas.
"""
from flask import Blueprint, request
from app.services import get_reservation_service
from app.utils.responses import success_response, error_response, not_found_response
from app.utils.validators import validate_reservation_data, parse_date

reservations_bp = Blueprint('reservations', __name__)
reservation_service = get_reservation_service()


@reservations_bp.route('', methods=['GET'])
def get_all_reservations():
    """
    GET /api/reservations
    Obtiene todas las reservas.
    
    Query params opcionales:
        - cabin_id: Filtrar por ID de cabaña
        - start_date: Filtrar por rango de fechas (inicio)
        - end_date: Filtrar por rango de fechas (fin)
    
    Returns:
        JSON con la lista de reservas
    """
    cabin_id = request.args.get('cabin_id', type=int)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    guest_name = request.args.get('guest_name')
    
    # Filtrar por cabaña si se especifica
    if cabin_id:
        reservations = reservation_service.get_by_cabin(cabin_id)
    # Filtrar por rango de fechas si se especifica
    elif start_date_str and end_date_str:
        start_date, error = parse_date(start_date_str)
        if error:
            return error_response(error)
        
        end_date, error = parse_date(end_date_str)
        if error:
            return error_response(error)
        
        reservations = reservation_service.get_by_date_range(start_date, end_date)
    elif guest_name:
        reservations = reservation_service.get_by_guest_name(guest_name)
    else:
        reservations = reservation_service.get_all()
    
    reservations_data = [r.to_dict() for r in reservations]
    
    return success_response(
        reservations_data,
        message=f"Se encontraron {len(reservations_data)} reservas"
    )


@reservations_bp.route('/<reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    """
    GET /api/reservations/<id>
    Obtiene una reserva específica por ID.
    
    Args:
        reservation_id: ID de la reserva
        
    Returns:
        JSON con los datos de la reserva
    """
    reservation = reservation_service.get_by_id(reservation_id)
    
    if not reservation:
        return not_found_response("Reserva", reservation_id)
    
    return success_response(reservation.to_dict())


@reservations_bp.route('', methods=['POST'])
def create_reservation():
    """
    POST /api/reservations
    Crea una nueva reserva.
    
    Body:
        {
            "cabin_id": int,
            "guest_name": str,
            "guest_email": str (opcional),
            "guest_phone": str (opcional),
            "start_date": str (YYYY-MM-DD),
            "end_date": str (YYYY-MM-DD),
            "num_guests": int,
            "notes": str (opcional)
        }
    
    Returns:
        JSON con la reserva creada
    """
    if not request.json:
        return error_response("Se requiere un body JSON")
    
    # Validar datos básicos
    validation_error = validate_reservation_data(request.json)
    if validation_error:
        return error_response(validation_error)
    
    # Parsear fechas
    start_date, error = parse_date(request.json['start_date'])
    if error:
        return error_response(error)
    
    end_date, error = parse_date(request.json['end_date'])
    if error:
        return error_response(error)
    
    # Preparar datos para crear la reserva
    reservation_data = {
        'cabin_id': int(request.json['cabin_id']),
        'guest_name': request.json['guest_name'].strip(),
        'guest_email': request.json.get('guest_email', '').strip(),
        'guest_phone': request.json.get('guest_phone', '').strip(),
        'start_date': start_date,
        'end_date': end_date,
        'num_guests': int(request.json['num_guests']),
        'notes': request.json.get('notes', '').strip()
    }
    
    # Crear la reserva
    reservation, error = reservation_service.create(reservation_data)
    
    if error:
        return error_response(error, status_code=400)
    
    return success_response(
        reservation.to_dict(),
        message="Reserva creada exitosamente",
        status_code=201
    )


@reservations_bp.route('/<reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    """
    PUT /api/reservations/<id>
    Actualiza una reserva existente.
    
    Args:
        reservation_id: ID de la reserva
        
    Body:
        JSON con los campos a actualizar
        
    Returns:
        JSON con la reserva actualizada
    """
    if not request.json:
        return error_response("Se requiere un body JSON")
    
    # Verificar que la reserva existe
    existing = reservation_service.get_by_id(reservation_id)
    if not existing:
        return not_found_response("Reserva", reservation_id)
    
    # Preparar datos de actualización
    update_data = {}
    
    # Campos que pueden actualizarse
    if 'cabin_id' in request.json:
        update_data['cabin_id'] = int(request.json['cabin_id'])
    
    if 'guest_name' in request.json:
        guest_name = request.json['guest_name'].strip()
        if len(guest_name) < 2:
            return error_response("El nombre del huésped debe tener al menos 2 caracteres")
        update_data['guest_name'] = guest_name
    
    if 'guest_email' in request.json:
        update_data['guest_email'] = request.json['guest_email'].strip()
    
    if 'guest_phone' in request.json:
        update_data['guest_phone'] = request.json['guest_phone'].strip()
    
    if 'start_date' in request.json:
        start_date, error = parse_date(request.json['start_date'])
        if error:
            return error_response(error)
        update_data['start_date'] = start_date
    
    if 'end_date' in request.json:
        end_date, error = parse_date(request.json['end_date'])
        if error:
            return error_response(error)
        update_data['end_date'] = end_date
    
    if 'num_guests' in request.json:
        num_guests = int(request.json['num_guests'])
        if num_guests < 1:
            return error_response("El número de huéspedes debe ser al menos 1")
        update_data['num_guests'] = num_guests
    
    if 'notes' in request.json:
        update_data['notes'] = request.json['notes'].strip()
    
    # Actualizar la reserva
    reservation, error = reservation_service.update(reservation_id, update_data)
    
    if error:
        return error_response(error, status_code=400)
    
    return success_response(
        reservation.to_dict(),
        message="Reserva actualizada exitosamente"
    )


@reservations_bp.route('/<reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    """
    DELETE /api/reservations/<id>
    Elimina una reserva.
    
    Args:
        reservation_id: ID de la reserva
        
    Returns:
        JSON con confirmación de eliminación
    """
    success = reservation_service.delete(reservation_id)
    
    if not success:
        return not_found_response("Reserva", reservation_id)
    
    return success_response(
        {'id': reservation_id},
        message="Reserva eliminada exitosamente"
    )
