from datetime import date
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Car:
    
    plate: str
    brand: str
    model: str
    year: int
    last_revision: Optional[date] = None
    
    
    def __post_init__(self):
        self.plate = self.plate.strip().upper()
        self.brand = self.brand.strip()
        self.model = self.model.strip()
        
        #Validaciones
        self._validate_plate()
        self._validate_brand_model()
        self._validate_year()
    
    #Metodo que valida la matricula de un coche con una expresion regular
    def _validate_plate(self):
        pattern = r'^[0-9]{4}[A-Z]{3}$'
        if not re.match(pattern, self.plate):
            raise ValueError(f"Formato de matricula incorrecto: {self.plate}")
    
    #Metodo que valida el año para que no sea menor de 1900 y mayor del año actual en el que estamos
    def _validate_year(self):
        current_year = date.today().year
        if not(1900 <= self.year <= current_year):
            raise ValueError(f"Fecha del coche no valida: {self.year}")
    
    #Metodo que valida si se deja en blanco la marca y el modelo
    def _validate_brand_model(self):
        if not self.brand:
            raise ValueError("Error la marca no puede estar vacia")
        
        if not self.model:
            raise ValueError("Error el modelo no puede etsar vacio")
    
    #Comprueba si ha pasado la revision y ademas si ha pasado el año o no
    def needs_revision(self) -> bool:
        if self.last_revision is None:
            return True
        
        days_passed = (date.today() - self.last_revision).days
        return days_passed >= 365
