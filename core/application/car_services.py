from typing import List, Optional

from core.domain.car import Car
from core.ports.car_repository import CarRepository

class RegisterCarService:
    
    """Caso de uso: registrar un nuevo coche en el sistema"""
    
    def __init__(self, car_repo: CarRepository) -> None:
        self._car_repo = car_repo
    
    def execute(self, car: Car) -> None:
        """Registrar un nuevo coche"""
        plate = car.plate
        
        existing = self._car_repo.get_by_plate(plate)
        if existing is not None:
            raise ValueError(f"Ya existe un coche con matricula {plate}")
        
        self._car_repo.add(car)

class GetCarByPlateService:
    """Obtener un coche por su matricula"""
    def __init__(self, car_repo: CarRepository) -> None:
        self._car_repo = car_repo
    
    def execute(self, raw_plate: str) -> Optional[Car]:
        plate = raw_plate.strip().upper()
        return self._car_repo.get_by_plate(plate)

class ListCarsService:
    """Caso de uso: listar todos los coches"""
    
    def __init__(self, car_repo: CarRepository) -> None:
        self._car_repo = car_repo
    
    def execute(self) -> List[Car]:
        """Devuelve la lista de coches"""
        return self._car_repo.list_all()


class UpdateCarsService:
    """Caso de uso: actualizar los datos de los coches registrados"""
    
    def __init__(self, car_repo: CarRepository) -> None:
        self._car_repo = car_repo
    
    
    def execute(self, car: Car) -> None:
        """Actualiza un coche"""
        plate = car.plate
        
        existing = self._car_repo.get_by_plate(plate)
        
        if existing is None:
            raise ValueError(f"No existe ningun coche con la matricula {plate}")
        
        self._car_repo.update(car)


class DeleteCarsService:
    """Caso de uso: borrar el coche"""
    
    def __init__(self, car_repo: CarRepository) -> None:
        self._car_repo = car_repo
    
    def execute(self, raw_plate: str) -> None:
        """Elimina un coche"""
        plate = raw_plate.strip().upper()
        
        self._car_repo.delete(plate)
