
from typing import List, Optional
from dataclasses import asdict
from datetime import date

from adapters.persistence.json_base import JsonRepositoryBase

from core.domain.car import Car


class CarJsonRepository(JsonRepositoryBase):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
    
    #Pasar de objeto a diccionario
    def _car_to_dict(self, car: Car) -> dict:
        """Convierte un Objeto Car a un diccionario compatible con JSON"""
        data = asdict(car)
        #Convertimos las fechas a texto para que lo entienda el JSON
        if car.last_revision:
            data['last_revision'] = car.last_revision.isoformat()
        return data
    
    def _dict_to_car(self, data: dict) -> Car:
        """Convierte un diccionario del JSON a un objeto Car"""
        if data.get('last_revision'):
            data['last_revision'] = date.fromisoformat(data['last_revision'])
        
        return Car(**data)
    
    #Implementacion del Protocolo
    def add(self, car: Car) -> None:
        cars_data = self._read_json()
        cars_data.append(self._car_to_dict(car))
        self._write_json(cars_data)
    
    def get_by_plate(self, plate: str) -> Optional[Car]:
        cars_data = self._read_json()
        for car_dict in cars_data:
            if car_dict.get('plate') == plate:
                return self._dict_to_car(car_dict)
        return None
    
    def list_all(self) -> List[Car]:
        cars_data = self._read_json()
        return [self._dict_to_car(d) for d in cars_data]
    
    def update(self, car: Car) -> None:
        cars_data = self._read_json()
        updated = False
        for i, car_dict in enumerate(cars_data):
            if car_dict.get('plate') == car.plate:
                cars_data[i] = self._car_to_dict(car)
                updated = True
                break
        if updated:
            self._write_json(cars_data)
    
    def delete(self, plate: str) -> None:
        cars_data = self._read_json()
        #Filtramos la lista nos quedamos con los que NO tengan esa matricula
        new_data = [c for c in cars_data if c.get('plate') != plate]
        self._write_json(new_data)