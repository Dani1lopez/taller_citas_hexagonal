from typing import List
from dataclasses import asdict
from datetime import date, time  

from adapters.persistence.json_base import JsonRepositoryBase

from core.domain.appointment import Appointment
from core.domain.car import Car
from core.domain.customer import Customer
from core.ports.car_repository import CarRepository
from core.ports.customer_repository import CustomerRepository

class AppointmentJsonRepository(JsonRepositoryBase):
    def __init__(self, file_path: str, customer_repo: CustomerRepository, car_repo: CarRepository) -> None:
        super().__init__(file_path)
        self._customer_repo = customer_repo
        self._car_repo = car_repo
    
    def _appointment_to_dict(self, app: Appointment) -> dict:
        """Guarda los IDs en lugar de los objetos completos"""
        data = asdict(app)
        
        # Remplazamos los objetos completos por sus claves primarias
        data['customer_dni'] = app.customer.dni
        data['car_plate'] = app.car.plate

        # --- CORRECCIÓN IMPORTANTE ---
        # Borramos los objetos completos para que no se guarden duplicados en el JSON
        del data['customer']
        del data['car']
        
        # Convertir Fecha y Hora a texto
        data['date'] = app.date.isoformat()
        data['time'] = app.time.isoformat()
        
        return data
    
    def _dict_to_appointment(self, data: dict) -> Appointment:
        data['date'] = date.fromisoformat(data['date'])
        # --- CORRECCIÓN IMPORTANTE ---
        # Usamos time.fromisoformat (NO date.fromisoformat)
        data['time'] = time.fromisoformat(data['time'])
        
        customer = self._customer_repo.get_by_dni(data['customer_dni'])
        car = self._car_repo.get_by_plate(data['car_plate'])
        
        # Objetos dummy por seguridad si no existen
        data['customer'] = customer if customer else Customer(dni="ERR", name="Unknown", surname="Unknown", birth_date=date.today(), email="e@e.com", phone="0")
        data['car'] = car if car else Car(plate="ERR", brand="Unknown", model="Unknown", year=2000, last_revision=None)
        
        del data['customer_dni']
        del data['car_plate']
        
        return Appointment(**data)
    
    def add(self, appointment: Appointment) -> None:
        data = self._read_json()
        data.append(self._appointment_to_dict(appointment))
        self._write_json(data)
    
    def list_all(self) -> List[Appointment]:
        data = self._read_json()
        return [self._dict_to_appointment(item) for item in data]
    
    def find_by_date(self, date_: date) -> List[Appointment]:
        """Busca y devuelve todas las citas de un dia concreto"""
        data = self._read_json()
        resultado = []
        target_date_str = date_.isoformat()
        
        for item in data:
            if item.get('date') == target_date_str:
                resultado.append(self._dict_to_appointment(item))
        return resultado
    
    def find_by_customer(self, dni: str) -> List[Appointment]:
        """Devuelve todas las citas pertenecientes a un cliente por su DNI"""
        data = self._read_json()
        resultado = []
        for item in data:
            if item.get('customer_dni') == dni:
                resultado.append(self._dict_to_appointment(item))
        return resultado
    
    def find_by_car(self, plate: str) -> List[Appointment]:
        """Devuelve todas las citas asociadas a una matricula concreta"""
        data = self._read_json()
        resultado = []
        for item in data:
            if item.get('car_plate') == plate:
                resultado.append(self._dict_to_appointment(item))
        return resultado
    
    def update(self, appointment: Appointment) -> None:
        """Actualiza una cita. Usamos (coche + fecha + hora) como identificador unico"""
        data = self._read_json()
        updated = False
        
        target_plate = appointment.car.plate
        target_date = appointment.date.isoformat()
        target_time = appointment.time.isoformat()
        
        for i, item in enumerate(data):
            if (item.get('car_plate') == target_plate and item.get('date') == target_date and item.get('time') == target_time):
                data[i] = self._appointment_to_dict(appointment)
                updated = True
                break
        
        if updated:
            self._write_json(data)
    
    def delete(self, appointment: Appointment) -> None:
        """Elimina la cita exacta"""
        data = self._read_json()
        
        target_plate = appointment.car.plate
        target_date = appointment.date.isoformat()
        target_time = appointment.time.isoformat()
        
        new_data = [
            item for item in data
            if not (item.get('car_plate') == target_plate and item.get('date') == target_date and item.get('time') == target_time)
        ]
        
        self._write_json(new_data)