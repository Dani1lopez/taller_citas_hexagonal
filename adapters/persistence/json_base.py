import json
import os
from typing import List, TypeVar

T = TypeVar('T')

class JsonRepositoryBase:
    """Clase base que maneja las operaciones CRUD básicas de JSON"""
    
    def __init__(self, file_path: str) -> None:
        """Configura la ruta del archivo y se asegura que existe"""
        self._file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Crea el archivo json vacio si no existe para evitar errores"""
        if not os.path.exists(self._file_path):
            with open(self._file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def _read_json(self) -> List[dict]:
        """Leer el archivo JSON y devuelve una lista de diccionarios"""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_json(self, data: List[dict]) -> None:
        """Escribe la lista de diccionarios en el archivo JSON"""
        with open(self._file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)