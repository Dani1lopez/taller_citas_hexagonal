from typing import Protocol, Optional, List
from core.domain.car import Car

class CarRepository(Protocol):
    
    def add(self, car: Car) -> None:
        """Guarda un nuevo coche"""
        ...
    
    def get_by_plate(self, plate: str) -> Optional[Car]:
        """Devuelve la matricula o none si existe"""
        ...
    
    def list_all(self) -> List[Car]:
        """Devuelve todos los car"""
        ...
    
    def update(self, car: Car) -> None:
        """Actualiza el coche"""
        ...
    
    def delete(self, plate: str) -> None:
        """Borra un coche"""
        ...