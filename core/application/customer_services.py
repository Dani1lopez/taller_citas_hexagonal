from typing import List, Optional

from core.domain.customer import Customer
from core.ports.customer_repository import CustomerRepository

class RegisterCustomerService:
    """Caso de uso para registrar un nuevo cliente"""
    def __init__(self, customer_repo: CustomerRepository) -> None:
        #El servicio no sabe si recibe un JSON, SQL, API ... 
        #Solo sabe que recibe algo que cumple CustomerRepository
        self.customer_repo = customer_repo
    
    
    def execute(self, customer: Customer) -> None:
        """Comprobamos si existe ya un cliente con ese DNI"""
        dni = customer.dni
        
        existing = self.customer_repo.get_by_dni(dni)
        if existing is not None:
            raise ValueError(f"Ya existe un cliente con DNI {dni}")
        
        self.customer_repo.add(customer)


class GetCustomerbyDniService:
    """Caso de uso: Obtener un cliente por el dni"""
    
    def __init__(self, customer_repo: CustomerRepository) -> None:
        self.customer_repo = customer_repo
    
    
    def execute(self, raw_dni: str) -> Optional[Customer]:
        """Devuelve el cliente con ese DNI o None si no existe"""
        dni = raw_dni.strip().upper()
        
        return self.customer_repo.get_by_dni(dni)


class ListCustomerService:
    
    def __init__(self, customer_repo: CustomerRepository) -> None:
        self.customer_repo = customer_repo
    
    
    def execute(self) -> List[Customer]:
        """Devuelve la lista completa de clientes"""
        return self.customer_repo.list_all()


class UpdateCustomerService:
    
    def __init__(self, customer_repo: CustomerRepository) -> None:
        self._customer_repo = customer_repo
    
    
    def execute(self, customer: Customer) -> None:
        """Actualiza un cliente"""
        dni = customer.dni
        
        #Comprobamos que exista
        existing = self._customer_repo.get_by_dni(dni)
        
        if existing is None:
            raise ValueError(f"No existe ningún cliente con el DNI {dni}")
        
        self._customer_repo.update(customer)


class DeleteCustomerService:
    
    def __init__(self, customer_repo: CustomerRepository) -> None:
        self._customer_repo = customer_repo
    
    def execute(self, raw_dni: str) -> None:
        """Elimina el cliente con ese DNI"""
        
        dni = raw_dni.strip().upper()
        
        self._customer_repo.delete(dni)