"""
Modelo de Cabaña.
Representa una cabaña individual del complejo.
"""
from typing import Dict, Any


class Cabin:
    """
    Clase que representa una cabaña en el complejo.
    
    Attributes:
        id (int): Identificador único de la cabaña
        name (str): Nombre descriptivo de la cabaña
        pair_group (int): Grupo de par al que pertenece (1-8, ya que hay 16 cabañas en 8 pares)
        capacity (int): Capacidad máxima de personas
        amenities (list): Lista de comodidades disponibles
    """
    
    def __init__(self, id: int, name: str, pair_group: int, capacity: int = 4, amenities: list = None):
        """
        Inicializa una nueva cabaña.
        
        Args:
            id: Identificador único
            name: Nombre de la cabaña
            pair_group: Número del grupo de par (1-8)
            capacity: Capacidad máxima de personas (default: 4)
            amenities: Lista de comodidades (default: [])
        """
        self.id = id
        self.name = name
        self.pair_group = pair_group
        self.capacity = capacity
        self.amenities = amenities or []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la cabaña a un diccionario para serialización JSON.
        
        Returns:
            Dict con los datos de la cabaña
        """
        return {
            'id': self.id,
            'name': self.name,
            'pair_group': self.pair_group,
            'capacity': self.capacity,
            'amenities': self.amenities
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Cabin':
        """
        Crea una instancia de Cabin desde un diccionario.
        
        Args:
            data: Diccionario con los datos de la cabaña
            
        Returns:
            Instancia de Cabin
        """
        return Cabin(
            id=data['id'],
            name=data['name'],
            pair_group=data['pair_group'],
            capacity=data.get('capacity', 4),
            amenities=data.get('amenities', [])
        )
    
    def __repr__(self):
        return f"<Cabin {self.id}: {self.name} (Pair {self.pair_group})>"
