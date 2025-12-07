from typing import List, Optional
from dataclasses import asdict
from datetime import date

from core.domain.customer import Customer
from adapters.persistence.json_base import JsonRepositoryBase

class CustomerJsonRepository(JsonRepositoryBase):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
    
    def _customer_to_dict(self, customer: Customer) -> dict:
        """Convierte Objeto Customer -> Diccionario JSON"""
        data = asdict(customer)
        #Convertimos la fecha de nacimiento a texto para guardarla
        data['birth_date'] = customer.birth_date.isoformat()
        return data
    
    def _dict_to_customer(self, data: dict) -> Customer:
        """Convierte Diccionario JSON -> Objeto Customer"""
        if data.get('birth_date'):
            data['birth_date'] = date.fromisoformat(data['birth_date'])
        
        #El doble asterisco desempaqueta el diccionario en argumentos nombrados
        return Customer(**data)
    
    #Implementacion del Protocolo CustomerRepository
    def add(self, customer: Customer) -> None:
        customers_data = self._read_json()
        customers_data.append(self._customer_to_dict(customer))
        self._write_json(customers_data)
    
    def get_by_dni(self, dni: str) -> Optional[Customer]:
        customers_data = self._read_json()
        for cust_dict in customers_data:
            if cust_dict.get('dni') == dni:
                return self._dict_to_customer(cust_dict)
        return None
    
    def list_all(self) -> List[Customer]:
        customers_data = self._read_json()
        return [self._dict_to_customer(d) for d in customers_data]
    
    def update(self, customer: Customer) -> None:
        customers_data = self._read_json()
        updated = False
        for i, cust_dict in enumerate(customers_data):
            if cust_dict.get('dni') == customer.dni:
                customers_data[i] = self._customer_to_dict(customer)
                updated = True
                break
        if updated:
            self._write_json(customers_data)
    
    def delete(self, dni: str) -> None:
        customers_data = self._read_json()
        new_data = [c for c in customers_data if c.get('dni') != dni]
        self._write_json(new_data)