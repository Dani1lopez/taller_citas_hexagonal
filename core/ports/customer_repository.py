from typing import Protocol, Optional, List
from core.domain.customer import Customer

class CustomerRepository(Protocol):
    """Contrato que debe de cumplir cualquier repositorio de clientes"""
    
    def add(self, customer: Customer) -> None:
        """Guarda un nuevo cliente. Lanza error si ya existe"""
        ...
    
    def get_by_dni(self, dni: str) -> Optional[Customer]:
        """Devuelve el cliente con ese DNI o None si no existe"""
        ...
    
    def list_all(self) -> List[Customer]:
        """Devuelve la lista completa de clientes"""
        ...
    
    def update(self, customer: Customer) -> None:
        """Actualiza un cliente existente"""
        ...
    
    def delete(self, dni: str) -> None:
        """Elimina el cliente con ese DNI (si existe)"""
        ...
