from datetime import date, time, datetime
from dataclasses import dataclass

from core.domain.customer import Customer
from core.domain.car import Car

@dataclass
class Appointment:
    
    customer: Customer
    car: Car
    date: date
    time: time
    cost: float
    
    def __post_init__(self):
        #Validaciones
        self._validate_time()
        self._validate_car()
        self._validate_cost()
        self._validate_date()
        self._validate_customer()
    
    
    #Validaciones protegidas
    
    #Valida que sea un objeto de customer
    def _validate_customer(self):
        if not isinstance(self.customer, Customer):
            raise TypeError("customer debe ser un objeto de Customer")
    
    def _validate_car(self):
        if not isinstance(self.car, Car):
            raise TypeError("car debe ser un objeto Car")
    
    def _validate_date(self):
        if not isinstance(self.date, date):
            raise TypeError("debe ser un objeto de datetime.date")
    
    def _validate_time(self):
        if not isinstance(self.time, time):
            raise TypeError("time debe ser un objeto datetime.time")
    
    def _validate_cost(self):
        if self.cost < 0:
            raise ValueError("El coste no puede ser negativo")
    
    
    #Reglas de Negocio
    
    def starts_at(self) -> datetime:
        """Devuelve la cita como un datetime completo"""
        return datetime.combine(self.date, self.time)
    
    def is_past(self) -> bool:
        """True si la cita ya pasó respecto al momento actual"""
        return self.starts_at() < datetime.now()
    
    def involves_car(self, plate: str) -> bool:
        """Devuelve True si la cita corresponde a esta matricula"""
        return self.car.plate == plate.upper()
    
    def involves_customer(self, dni: str) -> bool:
        """Devuelve True si la cita corresponde a este DNI"""
        return self.customer.dni == dni.upper()

