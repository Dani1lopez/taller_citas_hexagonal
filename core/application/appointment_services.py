from typing import List, Optional
from datetime import date, time

from core.domain.appointment import Appointment
from core.ports.appointment_repository import AppointmetRepository
from core.ports.customer_repository import CustomerRepository
from core.ports.car_repository import CarRepository

class SheduleAppointmentService:
    """Caso de uso: programar una nueva cita"""
    
    def __init__(self, appointmet_repo: AppointmetRepository, customer_repo: CustomerRepository, car_repo: CarRepository) -> None:
        self._appointments_repo = appointmet_repo
        self._customers_repo = customer_repo
        self._cars_repo = car_repo
    
    def execute(self, customer_dni: str, car_plate: str, date_: date, time_: time, cost:float) -> Appointment:
        dni = customer_dni.strip().upper()
        plate = car_plate.strip().upper()
        
        customer = self._customers_repo.get_by_dni(dni)
        if customer is None:
            raise ValueError(f"No existe ningún cliente con DNI {dni}")
        
        car = self._cars_repo.get_by_plate(plate)
        if car is None:
            raise ValueError(f"No existe ningún coche con matrícula {plate}")
        
        appointment = Appointment(
            customer = customer,
            car = car,
            date = date_,
            time = time_,
            cost = cost,
        )
        
        #Regla de negocio no permitir citas en el pasado
        if appointment.is_past():
            raise ValueError("No se puede crear una cita en el pasado")
        
        self._appointments_repo.add(appointment)
        return appointment


class ListAppointmentsByDateService:
    """Caso de uso: listar citas por fecha concreta"""
    def __init__(self, appointment_repo: AppointmetRepository) -> None:
        self._appointments = appointment_repo
    
    def execute(self, date_: Optional[date] = None) -> List[Appointment]:
        """Devuelve todas las citas de un dia concreto, o todas las citas si no se especifica fecha"""
        if date_ is None:
            return self._appointments.list_all()
        return self._appointments.find_by_date(date_)


class ListAppointmentsByCustomerService:
    """Caso de uso: listar citas de un cliente"""
    def __init__(self, appointment_repo: AppointmetRepository) -> None:
        self._appointments = appointment_repo
    
    def execute(self, raw_dni: str) -> List[Appointment]:
        """Devuelve todas las citas asociadas a un cliente por su DNI"""
        dni = raw_dni.strip().upper()
        return self._appointments.find_by_customer(dni)


class ListAppointmentsByCarService:
    """Caso de uso: listar citas de un coche"""
    def __init__(self, appointment_repo: AppointmetRepository) -> None:
        self._appointments = appointment_repo
    
    def execute(self, raw_plate: str) -> List[Appointment]:
        """Devuelve todas las citas asociadas a una matricula"""
        plate = raw_plate.strip().upper()
        return self._appointments.find_by_car(plate)


class UpdateAppointmentService:
    """Caso de uso: Actualizar la cita"""
    def __init__(self, appointment_repo: AppointmetRepository) -> None:
        self._appointments = appointment_repo
    
    def execute(self, appointment: Appointment) -> None:
        if appointment.is_past():
            raise ValueError("No se puede actulizar la cita a una fecha/hora pasada")
        
        self._appointments.update(appointment)


class DeleteAppointmentService:
    """Caso de uso: Eliminar una cita"""
    def __init__(self, appointment_repo: AppointmetRepository) -> None:
        self.appointment_repo = appointment_repo
    
    def execute(self, appointment: Appointment) -> None:
        self.appointment_repo.delete(appointment)
