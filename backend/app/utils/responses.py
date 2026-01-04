"""
Utilidades para formatear respuestas HTTP.
"""
from flask import jsonify
from typing import Any, Tuple


def success_response(data: Any, message: str = None, status_code: int = 200) -> Tuple[Any, int]:
    """
    Crea una respuesta exitosa estándar.
    
    Args:
        data: Datos a devolver
        message: Mensaje opcional
        status_code: Código de estado HTTP (default: 200)
        
    Returns:
        Tupla (respuesta_json, status_code)
    """
    response = {
        'success': True,
        'data': data
    }
    
    if message:
        response['message'] = message
    
    return jsonify(response), status_code


def error_response(message: str, status_code: int = 400, errors: dict = None) -> Tuple[Any, int]:
    """
    Crea una respuesta de error estándar.
    
    Args:
        message: Mensaje de error
        status_code: Código de estado HTTP (default: 400)
        errors: Diccionario opcional con detalles del error
        
    Returns:
        Tupla (respuesta_json, status_code)
    """
    response = {
        'success': False,
        'error': message
    }
    
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code


def not_found_response(resource: str, identifier: Any = None) -> Tuple[Any, int]:
    """
    Crea una respuesta estándar para recursos no encontrados.
    
    Args:
        resource: Nombre del recurso (ej: "Cabaña", "Reserva")
        identifier: Identificador del recurso (opcional)
        
    Returns:
        Tupla (respuesta_json, 404)
    """
    if identifier:
        message = f"{resource} con ID '{identifier}' no encontrada"
    else:
        message = f"{resource} no encontrada"
    
    return error_response(message, status_code=404)
