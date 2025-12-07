from typing import Protocol, List
from core.domain.appointment import Appointment
from datetime import date


class AppointmetRepository(Protocol):
    
    def add(self, appointment: Appointment) -> None:
        """Crea una nueva cita"""
        ...
    
    def list_all(self) -> List[Appointment]:
        """Devuelve todas las citas"""
        ...
    
    def find_by_date(self, date_: date) -> List[Appointment]:
        """Busca y devuelve todas las citas de un dia concreto"""
        ...
    
    def find_by_customer(self, dni: str) -> List[Appointment]:
        """Devuelve todas las citas pertenecientes a un cliente por su DNI"""
        ...
    
    def find_by_car(self, plate: str) -> List[Appointment]:
        """Devuelve todas las citas asociadas a una matricula concreta"""
        ...
    
    def update(self, appointment: Appointment) -> None:
        """Actualiza un cita existente"""
        ...
    
    def delete(self, appointment: Appointment) -> None:
        """Elimina del sistema la cita exacta que se le pasa"""
        ...
