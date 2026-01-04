"""
Servicio de gestión de Reservas.
Maneja el almacenamiento y operaciones CRUD de reservas en memoria con validación de conflictos.
"""
from typing import List, Optional
from datetime import date
from app.models.reservation import Reservation
from app.services.cabin_service import get_cabin_service


class ReservationService:
    """
    Servicio para gestionar reservas.
    Utiliza almacenamiento en memoria (listas y diccionarios).
    
    Nota de migración a BD:
    Esta clase está diseñada para ser fácilmente reemplazable por una capa de
    persistencia basada en base de datos. Los métodos mantienen una interfaz
    consistente que no cambiaría significativamente al migrar.
    """
    
    def __init__(self):
        """Inicializa el servicio con almacenamiento en memoria."""
        self._reservations = {}  # Dict[str, Reservation]
        self._cabin_service = get_cabin_service()
    
    def create(self, reservation_data: dict) -> tuple[Optional[Reservation], Optional[str]]:
        """
        Crea una nueva reserva.
        
        Args:
            reservation_data: Diccionario con los datos de la reserva
            
        Returns:
            Tupla (reserva_creada, error_mensaje)
            Si hay error, reserva_creada es None y error_mensaje contiene el error
        """
        try:
            # Validar que la cabaña existe
            cabin_id = reservation_data.get('cabin_id')
            if not self._cabin_service.exists(cabin_id):
                return None, f"La cabaña con ID {cabin_id} no existe"
            
            # Crear la reserva (esto valida las fechas)
            reservation = Reservation.from_dict(reservation_data)
            
            # Verificar conflictos con reservas existentes
            conflict = self._check_conflicts(reservation)
            if conflict:
                return None, (
                    f"Conflicto de fechas: la cabaña {cabin_id} ya está reservada "
                    f"del {conflict.start_date} al {conflict.end_date} "
                    f"por {conflict.guest_name}"
                )
            
            # Validar capacidad
            cabin = self._cabin_service.get_by_id(cabin_id)
            if reservation.num_guests > cabin.capacity:
                return None, (
                    f"La cabaña {cabin.name} tiene capacidad para {cabin.capacity} personas, "
                    f"pero se intentó reservar para {reservation.num_guests}"
                )

            # Restricción especial: cabañas 21–24 máximo 4 días
            if cabin_id in {21, 22, 23, 24}:
                if reservation.get_duration_days() > 4:
                    return None, (
                        f"{cabin.name} solo permite reservas de hasta 4 días"
                    )
            
            # Guardar la reserva en memoria
            self._reservations[reservation.id] = reservation
            return reservation, None
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error al crear la reserva: {str(e)}"
    
    def get_all(self) -> List[Reservation]:
        """
        Obtiene todas las reservas.
        
        Returns:
            Lista de todas las reservas ordenadas por fecha de inicio
        """
        reservations = list(self._reservations.values())
        return sorted(reservations, key=lambda r: r.start_date)
    
    def get_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """
        Obtiene una reserva por su ID.
        
        Args:
            reservation_id: ID de la reserva
            
        Returns:
            La reserva si existe, None en caso contrario
        """
        return self._reservations.get(reservation_id)
    
    def get_by_cabin(self, cabin_id: int) -> List[Reservation]:
        """
        Obtiene todas las reservas de una cabaña específica.
        
        Args:
            cabin_id: ID de la cabaña
            
        Returns:
            Lista de reservas de la cabaña ordenadas por fecha
        """
        reservations = [r for r in self._reservations.values() if r.cabin_id == cabin_id]
        return sorted(reservations, key=lambda r: r.start_date)
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Reservation]:
        """
        Obtiene todas las reservas que se solapan con un rango de fechas.
        
        Args:
            start_date: Fecha de inicio del rango
            end_date: Fecha de término del rango
            
        Returns:
            Lista de reservas que se solapan con el rango
        """
        return [r for r in self._reservations.values() if r.overlaps_with_range(start_date, end_date)]

    def get_by_guest_name(self, guest_name: str) -> List[Reservation]:
        """
        Obtiene reservas filtrando por nombre del huésped (substring, case-insensitive).
        """
        if not guest_name:
            return self.get_all()
        q = guest_name.strip().lower()
        reservations = [
            r for r in self._reservations.values()
            if q in (r.guest_name or '').lower()
        ]
        return sorted(reservations, key=lambda r: (r.start_date, r.cabin_id))
    
    def update(self, reservation_id: str, update_data: dict) -> tuple[Optional[Reservation], Optional[str]]:
        """
        Actualiza una reserva existente.
        
        Args:
            reservation_id: ID de la reserva a actualizar
            update_data: Diccionario con los datos a actualizar
            
        Returns:
            Tupla (reserva_actualizada, error_mensaje)
        """
        existing = self.get_by_id(reservation_id)
        if not existing:
            return None, "La reserva no existe"
        
        try:
            # Crear una nueva reserva con los datos actualizados
            merged_data = {
                'id': existing.id,
                'cabin_id': update_data.get('cabin_id', existing.cabin_id),
                'guest_name': update_data.get('guest_name', existing.guest_name),
                'guest_email': update_data.get('guest_email', existing.guest_email),
                'guest_phone': update_data.get('guest_phone', existing.guest_phone),
                'start_date': update_data.get('start_date', existing.start_date.isoformat()),
                'end_date': update_data.get('end_date', existing.end_date.isoformat()),
                'num_guests': update_data.get('num_guests', existing.num_guests),
                'notes': update_data.get('notes', existing.notes),
                'created_at': existing.created_at.isoformat()
            }
            
            updated_reservation = Reservation.from_dict(merged_data)
            
            # Validar que la cabaña existe
            if not self._cabin_service.exists(updated_reservation.cabin_id):
                return None, f"La cabaña con ID {updated_reservation.cabin_id} no existe"
            
            # Verificar conflictos (excluyendo esta misma reserva)
            conflict = self._check_conflicts(updated_reservation, exclude_id=reservation_id)
            if conflict:
                return None, (
                    f"Conflicto de fechas: la cabaña {updated_reservation.cabin_id} ya está reservada "
                    f"del {conflict.start_date} al {conflict.end_date} "
                    f"por {conflict.guest_name}"
                )
            
            # Validar capacidad
            cabin = self._cabin_service.get_by_id(updated_reservation.cabin_id)
            if updated_reservation.num_guests > cabin.capacity:
                return None, (
                    f"La cabaña {cabin.name} tiene capacidad para {cabin.capacity} personas, "
                    f"pero se intentó reservar para {updated_reservation.num_guests}"
                )

            # Restricción especial: cabañas 21–24 máximo 4 días
            if updated_reservation.cabin_id in {21, 22, 23, 24}:
                if updated_reservation.get_duration_days() > 4:
                    return None, (
                        f"{cabin.name} solo permite reservas de hasta 4 días"
                    )
            
            # Actualizar en memoria
            self._reservations[reservation_id] = updated_reservation
            return updated_reservation, None
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error al actualizar la reserva: {str(e)}"
    
    def delete(self, reservation_id: str) -> bool:
        """
        Elimina una reserva.
        
        Args:
            reservation_id: ID de la reserva a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        if reservation_id in self._reservations:
            del self._reservations[reservation_id]
            return True
        return False
    
    def check_availability(self, cabin_id: int, start_date: date, end_date: date) -> bool:
        """
        Verifica si una cabaña está disponible en un rango de fechas.
        
        Args:
            cabin_id: ID de la cabaña
            start_date: Fecha de inicio
            end_date: Fecha de término
            
        Returns:
            True si está disponible, False en caso contrario
        """
        cabin_reservations = self.get_by_cabin(cabin_id)
        for reservation in cabin_reservations:
            if reservation.overlaps_with_range(start_date, end_date):
                return False
        return True
    
    def get_available_cabins(self, start_date: date, end_date: date) -> List[int]:
        """
        Obtiene la lista de IDs de cabañas disponibles en un rango de fechas.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de término
            
        Returns:
            Lista de IDs de cabañas disponibles
        """
        all_cabins = self._cabin_service.get_all()
        available = []
        
        for cabin in all_cabins:
            if self.check_availability(cabin.id, start_date, end_date):
                available.append(cabin.id)
        
        return available
    
    def _check_conflicts(self, reservation: Reservation, exclude_id: Optional[str] = None) -> Optional[Reservation]:
        """
        Verifica si una reserva tiene conflictos con reservas existentes.
        
        Args:
            reservation: Reserva a verificar
            exclude_id: ID de reserva a excluir de la verificación (útil para updates)
            
        Returns:
            La primera reserva con conflicto encontrada, o None si no hay conflictos
        """
        cabin_reservations = self.get_by_cabin(reservation.cabin_id)
        for existing in cabin_reservations:
            if exclude_id and existing.id == exclude_id:
                continue
            if reservation.overlaps_with(existing):
                return existing
        return None


# Instancia singleton del servicio
_reservation_service_instance = None

def get_reservation_service() -> ReservationService:
    """
    Obtiene la instancia singleton del servicio de reservas.
    
    Returns:
        Instancia de ReservationService
    """
    global _reservation_service_instance
    if _reservation_service_instance is None:
        _reservation_service_instance = ReservationService()
    return _reservation_service_instance
