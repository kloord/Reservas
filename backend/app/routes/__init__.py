"""
Inicialización del paquete routes.
"""
from app.routes.cabins import cabins_bp
from app.routes.reservations import reservations_bp
from app.routes.availability import availability_bp

__all__ = ['cabins_bp', 'reservations_bp', 'availability_bp']
