"""
Servicio de gestión de Cabañas.
Maneja el almacenamiento y operaciones CRUD de cabañas en memoria.
"""
from typing import List, Optional
from app.models.cabin import Cabin


class CabinService:
    """
    Servicio para gestionar cabañas.
    Utiliza almacenamiento en memoria (listas y diccionarios).
    
    Nota de migración a BD:
    Esta clase está diseñada para ser fácilmente reemplazable por una capa de
    persistencia basada en base de datos (SQLAlchemy, por ejemplo).
    Los métodos mantienen una interfaz consistente que no cambiaría al migrar.
    """
    
    def __init__(self):
        """Inicializa el servicio con datos en memoria."""
        self._cabins = {}  # Dict[int, Cabin]
        self._initialize_cabins()
    
    def _initialize_cabins(self):
        """
        Inicializa las 16 cabañas del complejo organizadas en 8 pares.
        En producción, estos datos vendrían de una base de datos.
        """
        # Nombres: "Cabaña X" para IDs 1..16
        cabin_names = [
            ("Cabaña 1", "Cabaña 2"),
            ("Cabaña 3", "Cabaña 4"),
            ("Cabaña 5", "Cabaña 6"),
            ("Cabaña 7", "Cabaña 8"),
            ("Cabaña 9", "Cabaña 10"),
            ("Cabaña 11", "Cabaña 12"),
            ("Cabaña 13", "Cabaña 14"),
            ("Cabaña 15", "Cabaña 16")
        ]
        
        amenities_list = [
            ["Chimenea", "Cocina equipada", "Wi-Fi", "Parrilla"],
            ["Jacuzzi", "Cocina equipada", "Wi-Fi", "Terraza"],
            ["Vista al río", "Cocina equipada", "Wi-Fi", "Parrilla"],
            ["Cocina equipada", "Wi-Fi", "Terraza amplia", "Parrilla"],
            ["Chimenea", "Cocina equipada", "Wi-Fi", "Calefacción"],
            ["Cocina equipada", "Wi-Fi", "Vista panorámica", "Parrilla"],
            ["Jacuzzi", "Cocina equipada", "Wi-Fi", "Terraza"],
            ["Chimenea", "Cocina equipada", "Wi-Fi", "Jardín privado"]
        ]
        
        cabin_id = 1
        for pair_group, (name1, name2) in enumerate(cabin_names, start=1):
            # Primera cabaña del par
            self._cabins[cabin_id] = Cabin(
                id=cabin_id,
                name=name1,
                pair_group=pair_group,
                capacity=4,
                amenities=amenities_list[pair_group - 1]
            )
            cabin_id += 1
            
            # Segunda cabaña del par
            self._cabins[cabin_id] = Cabin(
                id=cabin_id,
                name=name2,
                pair_group=pair_group,
                capacity=4,
                amenities=amenities_list[pair_group - 1]
            )
            cabin_id += 1

        # Agregar cabañas funcionales adicionales 21–24 (dos pares)
        extra_amenities = ["Cocina equipada", "Wi-Fi"]
        self._cabins[21] = Cabin(id=21, name="Cabaña Express 21", pair_group=9, capacity=4, amenities=extra_amenities)
        self._cabins[22] = Cabin(id=22, name="Cabaña Express 22", pair_group=9, capacity=4, amenities=extra_amenities)
        self._cabins[23] = Cabin(id=23, name="Cabaña Express 23", pair_group=10, capacity=4, amenities=extra_amenities)
        self._cabins[24] = Cabin(id=24, name="Cabaña Express 24", pair_group=10, capacity=4, amenities=extra_amenities)
    
    def get_all(self) -> List[Cabin]:
        """
        Obtiene todas las cabañas.
        
        Returns:
            Lista de todas las cabañas
        """
        return list(self._cabins.values())
    
    def get_by_id(self, cabin_id: int) -> Optional[Cabin]:
        """
        Obtiene una cabaña por su ID.
        
        Args:
            cabin_id: ID de la cabaña
            
        Returns:
            La cabaña si existe, None en caso contrario
        """
        return self._cabins.get(cabin_id)
    
    def get_by_pair_group(self, pair_group: int) -> List[Cabin]:
        """
        Obtiene las cabañas de un grupo de par específico.
        
        Args:
            pair_group: Número del grupo de par (1-8)
            
        Returns:
            Lista de cabañas del par
        """
        return [cabin for cabin in self._cabins.values() if cabin.pair_group == pair_group]
    
    def exists(self, cabin_id: int) -> bool:
        """
        Verifica si existe una cabaña con el ID dado.
        
        Args:
            cabin_id: ID de la cabaña
            
        Returns:
            True si existe, False en caso contrario
        """
        return cabin_id in self._cabins
    
    def update(self, cabin_id: int, data: dict) -> Optional[Cabin]:
        """
        Actualiza los datos de una cabaña.
        
        Args:
            cabin_id: ID de la cabaña a actualizar
            data: Diccionario con los datos a actualizar
            
        Returns:
            La cabaña actualizada si existe, None en caso contrario
        """
        cabin = self._cabins.get(cabin_id)
        if not cabin:
            return None
        if 'name' in data:
            cabin.name = data['name']
        if 'capacity' in data:
            cabin.capacity = data['capacity']
        if 'amenities' in data:
            cabin.amenities = data['amenities']
        if 'pair_group' in data:
            cabin.pair_group = data['pair_group']
        return cabin


# Instancia singleton del servicio
# En una aplicación real con BD, esto se manejaría con dependency injection
_cabin_service_instance = None

def get_cabin_service() -> CabinService:
    """
    Obtiene la instancia singleton del servicio de cabañas.
    
    Returns:
        Instancia de CabinService
    """
    global _cabin_service_instance
    if _cabin_service_instance is None:
        _cabin_service_instance = CabinService()
    return _cabin_service_instance
