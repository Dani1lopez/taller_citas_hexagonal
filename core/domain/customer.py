from datetime import date
from dataclasses import dataclass
import re

@dataclass
class Customer:
    
    dni: str
    name: str
    surname: str
    birth_date: date
    email: str
    phone: str
    
    def __post_init__(self):
        #Normalizamos
        self.dni = self.dni.strip().upper()
        self.name = self.name.strip().capitalize()
        self.surname = self.surname.strip().title()
        self.email = self.email.strip().lower()
        self.phone = self.phone.strip()
        
        #Validaciones
        self._validate_dni()
        self._validate_email()
        self._validate_phone()
        self._validate_birth_date()
    
    #Validaciones protegidas
    
    #Validamos que tenga el formato correcto el dni con 8 numeros y una letra
    def _validate_dni(self):
        pattern = r'^[0-9]{8}[A-Z]$'
        if not re.match(pattern, self.dni):
            raise ValueError(f"El formato del dni no es valido {self.dni}")
    
    #Metodo que valida que tenga el formato corecto el email
    def _validate_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, self.email):
            raise ValueError("El formato de email no es valido")
    
    #Metodo valida el telefono
    def _validate_phone(self):
        if not self.phone.isdigit():
            raise ValueError("Solo puede contener numeros")
        
        if not(9<= len(self.phone) <= 15):
            raise ValueError("Tiene que tner entre 9 y 15 digitos")
    
    def _validate_birth_date(self):
        """La fecha no puede estar en el futuro"""
        if self.birth_date > date.today():
            raise ValueError("La fecha de nacimiento no puede ser despues de la fecha actual")
    
    #Regla de negocio
    
    def age(self) -> int:
        """Devuelve la edad actual del cliente"""
        today = date.today()
        years = today.year - self.birth_date.year
        
        if(today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        
        return years

