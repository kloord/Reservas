"""
Utilidades para validación de datos de entrada.
"""
from datetime import datetime, date
from typing import Tuple, Optional


def parse_date(date_string: str) -> Tuple[Optional[date], Optional[str]]:
    """
    Parsea una cadena de fecha en formato ISO (YYYY-MM-DD).
    
    Args:
        date_string: Cadena con la fecha
        
    Returns:
        Tupla (fecha_parseada, error_mensaje)
    """
    if not date_string:
        return None, "La fecha es requerida"
    
    try:
        parsed_date = datetime.fromisoformat(date_string).date()
        return parsed_date, None
    except ValueError:
        return None, f"Formato de fecha inválido: {date_string}. Use formato YYYY-MM-DD"


def validate_date_range(start_date: date, end_date: date) -> Optional[str]:
    """
    Valida que un rango de fechas sea válido.
    
    Args:
        start_date: Fecha de inicio
        end_date: Fecha de término
        
    Returns:
        Mensaje de error si hay problema, None si es válido
    """
    if start_date >= end_date:
        return "La fecha de inicio debe ser anterior a la fecha de término"
    
    return None


def validate_reservation_data(data: dict) -> Optional[str]:
    """
    Valida los datos básicos de una reserva.
    
    Args:
        data: Diccionario con los datos de la reserva
        
    Returns:
        Mensaje de error si hay problema, None si es válido
    """
    required_fields = ['cabin_id', 'guest_name', 'start_date', 'end_date', 'num_guests']
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            return f"El campo '{field}' es requerido"
    
    # Validar tipos
    try:
        cabin_id = int(data['cabin_id'])
        if cabin_id < 1:
            return "El ID de cabaña debe ser un número positivo"
    except (ValueError, TypeError):
        return "El ID de cabaña debe ser un número válido"
    
    try:
        num_guests = int(data['num_guests'])
        if num_guests < 1:
            return "El número de huéspedes debe ser al menos 1"
    except (ValueError, TypeError):
        return "El número de huéspedes debe ser un número válido"
    
    # Validar longitud del nombre
    guest_name = data['guest_name'].strip()
    if len(guest_name) < 2:
        return "El nombre del huésped debe tener al menos 2 caracteres"
    
    return None
