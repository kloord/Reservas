"""
Modelo de Reserva.
Gestiona las reservas de cabañas con validación de fechas y detección de conflictos.
"""
from datetime import datetime, date
from typing import Dict, Any, Optional
import uuid


class Reservation:
    """
    Clase que representa una reserva de cabaña.
    
    Attributes:
        id (str): Identificador único de la reserva (UUID)
        cabin_id (int): ID de la cabaña reservada
        guest_name (str): Nombre del huésped
        guest_email (str): Email del huésped
        guest_phone (str): Teléfono del huésped
        start_date (date): Fecha de inicio de la reserva
        end_date (date): Fecha de término de la reserva
        num_guests (int): Número de personas
        notes (str): Notas adicionales
        created_at (datetime): Fecha de creación de la reserva
    """
    
    def __init__(
        self,
        cabin_id: int,
        guest_name: str,
        start_date: date,
        end_date: date,
        num_guests: int,
        guest_email: str = "",
        guest_phone: str = "",
        notes: str = "",
        id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        """
        Inicializa una nueva reserva.
        
        Args:
            cabin_id: ID de la cabaña a reservar
            guest_name: Nombre del huésped
            start_date: Fecha de inicio
            end_date: Fecha de término
            num_guests: Número de personas
            guest_email: Email del huésped (opcional)
            guest_phone: Teléfono del huésped (opcional)
            notes: Notas adicionales (opcional)
            id: ID de la reserva (se genera si no se proporciona)
            created_at: Fecha de creación (se genera si no se proporciona)
            
        Raises:
            ValueError: Si las fechas son inválidas
        """
        # Validar fechas
        if not isinstance(start_date, date) or not isinstance(end_date, date):
            raise ValueError("Las fechas deben ser objetos date válidos")
        
        if start_date >= end_date:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de término")
        
        if start_date < date.today():
            raise ValueError("No se pueden crear reservas con fechas en el pasado")
        
        if num_guests < 1:
            raise ValueError("El número de huéspedes debe ser al menos 1")
        
        self.id = id or str(uuid.uuid4())
        self.cabin_id = cabin_id
        self.guest_name = guest_name
        self.guest_email = guest_email
        self.guest_phone = guest_phone
        self.start_date = start_date
        self.end_date = end_date
        self.num_guests = num_guests
        self.notes = notes
        self.created_at = created_at or datetime.now()
    
    def overlaps_with(self, other: 'Reservation') -> bool:
        """
        Verifica si esta reserva se solapa con otra reserva.
        
        Args:
            other: Otra reserva para comparar
            
        Returns:
            True si hay solapamiento, False en caso contrario
        """
        # No hay solapamiento si son de cabañas diferentes
        if self.cabin_id != other.cabin_id:
            return False
        
        # Dos rangos se solapan si:
        # - El inicio de uno está dentro del rango del otro, O
        # - El término de uno está dentro del rango del otro, O
        # - Uno contiene completamente al otro
        return (
            (self.start_date < other.end_date and self.end_date > other.start_date) or
            (other.start_date < self.end_date and other.end_date > self.start_date)
        )
    
    def overlaps_with_range(self, start_date: date, end_date: date) -> bool:
        """
        Verifica si esta reserva se solapa con un rango de fechas dado.
        
        Args:
            start_date: Fecha de inicio del rango
            end_date: Fecha de término del rango
            
        Returns:
            True si hay solapamiento, False en caso contrario
        """
        return (
            (self.start_date < end_date and self.end_date > start_date) or
            (start_date < self.end_date and end_date > self.start_date)
        )
    
    def get_duration_days(self) -> int:
        """
        Calcula la duración de la reserva en días.
        
        Returns:
            Número de días de la reserva
        """
        return (self.end_date - self.start_date).days
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la reserva a un diccionario para serialización JSON.
        
        Returns:
            Dict con los datos de la reserva
        """
        return {
            'id': self.id,
            'cabin_id': self.cabin_id,
            'guest_name': self.guest_name,
            'guest_email': self.guest_email,
            'guest_phone': self.guest_phone,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'num_guests': self.num_guests,
            'notes': self.notes,
            'duration_days': self.get_duration_days(),
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Reservation':
        """
        Crea una instancia de Reservation desde un diccionario.
        
        Args:
            data: Diccionario con los datos de la reserva
            
        Returns:
            Instancia de Reservation
            
        Raises:
            ValueError: Si los datos son inválidos
        """
        # Parsear fechas
        if isinstance(data['start_date'], str):
            start_date = datetime.fromisoformat(data['start_date']).date()
        else:
            start_date = data['start_date']
        
        if isinstance(data['end_date'], str):
            end_date = datetime.fromisoformat(data['end_date']).date()
        else:
            end_date = data['end_date']
        
        # Parsear created_at si existe
        created_at = None
        if 'created_at' in data:
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'])
            else:
                created_at = data['created_at']
        
        return Reservation(
            id=data.get('id'),
            cabin_id=data['cabin_id'],
            guest_name=data['guest_name'],
            guest_email=data.get('guest_email', ''),
            guest_phone=data.get('guest_phone', ''),
            start_date=start_date,
            end_date=end_date,
            num_guests=data['num_guests'],
            notes=data.get('notes', ''),
            created_at=created_at
        )
    
    def __repr__(self):
        return f"<Reservation {self.id}: Cabin {self.cabin_id} - {self.guest_name} ({self.start_date} to {self.end_date})>"
