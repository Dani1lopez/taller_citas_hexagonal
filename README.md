# 🚗 Sistema de Gestión de Citas para Taller Mecánico

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal-green.svg)](https://alistair.cockburn.us/hexagonal-architecture/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema completo de gestión de citas para talleres mecánicos desarrollado con **Arquitectura Hexagonal** (Ports & Adapters) y una moderna interfaz gráfica en **Tkinter**. Permite gestionar clientes, vehículos y citas de forma eficiente con persistencia en JSON.

![Demo Screenshot](https://via.placeholder.com/800x450/1a1a2e/16c79a?text=Sistema+de+Gestión+de+Taller)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación Técnica](#-documentación-técnica)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## ✨ Características

### 📊 Gestión Completa

- ✅ **Gestión de Clientes**: Registro, edición, eliminación y listado de clientes
- ✅ **Gestión de Vehículos**: Control completo de coches asociados a clientes
- ✅ **Gestión de Citas**: Programación, modificación y eliminación de citas de taller
- ✅ **Validación de Datos**: Validación robusta de DNI, email, teléfono y fechas
- ✅ **Búsqueda y Filtrado**: Sistema de búsqueda integrado en todas las secciones

### 🎨 Interfaz Moderna

- 🌙 **Tema Dark**: Diseño oscuro profesional con colores personalizados
- 💫 **Efectos Visuales**: Animaciones suaves y efectos hover
- 📱 **Diseño Responsivo**: Distribución optimizada con grid y scrollbars
- 🎯 **UX Mejorada**: Feedback visual para todas las acciones del usuario

### 🏗️ Arquitectura Robusta

- 🔷 **Hexagonal Architecture**: Separación clara entre dominio, casos de uso y adaptadores
- 🔌 **Inyección de Dependencias**: Bajo acoplamiento y alta cohesión
- 📦 **Persistencia JSON**: Sistema de almacenamiento simple y extensible
- 🧪 **Testeable**: Arquitectura que facilita pruebas unitarias

---

## 🏛️ Arquitectura

Este proyecto implementa **Arquitectura Hexagonal** (también conocida como Ports & Adapters), lo que permite:

```
┌─────────────────────────────────────────────────────────────┐
│                      ADAPTERS (UI)                          │
│                   tkinter_main.py                           │
│                   tkinter_forms.py                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│               APPLICATION (Use Cases)                       │
│     customer_services.py | car_services.py                  │
│              appointment_services.py                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                  DOMAIN (Entities)                          │
│     Customer | Car | Appointment                            │
│           + Business Rules                                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                 PORTS (Interfaces)                          │
│  customer_repository | car_repository                       │
│          appointment_repository                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│            ADAPTERS (Persistence)                           │
│         JSON Repositories Implementation                    │
└─────────────────────────────────────────────────────────────┘
```

### Beneficios de esta Arquitectura

1. **Independencia de frameworks**: La lógica de negocio no depende de Tkinter o JSON
2. **Fácil testing**: Se pueden testear casos de uso sin UI ni base de datos
3. **Flexibilidad**: Fácil cambiar de JSON a SQL, o de Tkinter a Web
4. **Mantenibilidad**: Código organizado y fácil de entender

---

## 🔧 Requisitos

- **Python**: 3.8 o superior
- **Tkinter**: Incluido con Python (normalmente viene preinstalado)
- **Sistema Operativo**: Windows, macOS, Linux

### Dependencias Python

```bash
# Tkinter suele venir incluido, pero si necesitas instalarlo:
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (con Homebrew)
brew install python-tk

# Windows: viene incluido con Python
```

---

## 📦 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Dani1lopez/taller_citas_hexagonal.git
cd taller_citas_hexagonal
```

### 2. Verificar Python

```bash
python --version
# Debe ser 3.8 o superior
```

### 3. (Opcional) Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Ejecutar la Aplicación

```bash
python main.py
```

---

## 🚀 Uso

### Inicio Rápido

1. **Ejecuta la aplicación**:

   ```bash
   python main.py
   ```

2. **Interfaz principal**: Verás tres pestañas principales:
   - 👥 **Clientes**: Gestiona la información de tus clientes
   - 🚗 **Coches**: Administra los vehículos asociados
   - 📅 **Citas**: Programa y gestiona las citas del taller

### Flujo de Trabajo Típico

1. **Registrar un Cliente**:

   - Ir a la pestaña "Clientes"
   - Completar el formulario (DNI, nombre, apellidos, fecha de nacimiento, email, teléfono)
   - Click en "Registrar Cliente"

2. **Añadir un Vehículo**:

   - Ir a la pestaña "Coches"
   - Seleccionar el cliente propietario
   - Introducir matrícula, marca, modelo y año
   - Click en "Registrar Coche"

3. **Crear una Cita**:
   - Ir a la pestaña "Citas"
   - Seleccionar fecha, hora, cliente y coche
   - Introducir descripción del servicio y coste estimado
   - Click en "Agendar Cita"

### Funcionalidades Avanzadas

- **Buscar**: Usa la barra de búsqueda en cada sección para filtrar registros
- **Editar**: Selecciona un elemento de la lista y click en "Editar"
- **Eliminar**: Selecciona un elemento y click en "Eliminar" (con confirmación)
- **Ordenar**: Las listas se ordenan automáticamente por relevancia

---

## 📁 Estructura del Proyecto

```
taller_citas/
│
├── core/                           # Núcleo del negocio (Hexágono Interior)
│   ├── domain/                     # Entidades de dominio
│   │   ├── customer.py            # Entidad Cliente con validaciones
│   │   ├── car.py                 # Entidad Coche
│   │   └── appointment.py         # Entidad Cita
│   │
│   ├── application/               # Casos de uso (Application Services)
│   │   ├── customer_services.py  # Servicios de cliente
│   │   ├── car_services.py       # Servicios de coche
│   │   └── appointment_services.py # Servicios de citas
│   │
│   └── ports/                     # Interfaces (Puertos)
│       ├── customer_repository.py
│       ├── car_repository.py
│       └── appointment_repository.py
│
├── adapters/                      # Adaptadores (Hexágono Exterior)
│   ├── persistence/              # Adaptadores de persistencia
│   │   ├── json_base.py         # Base para repositorios JSON
│   │   ├── customer_json_repository.py
│   │   ├── car_json_repository.py
│   │   └── appointment_json_repository.py
│   │
│   └── ui/                       # Adaptadores de UI
│       ├── tkinter_main.py      # Ventana principal
│       ├── tkinter_forms.py     # Formularios
│       └── ui_helpers.py        # Utilidades UI
│
├── data/                         # Almacenamiento JSON
│   ├── customers.json
│   ├── cars.json
│   └── appointments.json
│
├── main.py                       # Punto de entrada (Composition Root)
├── test_forms.py                 # Tests de formularios
└── README.md                     # Este archivo
```

---

## 📚 Documentación Técnica

### Dominio (`core/domain/`)

Las entidades de dominio contienen la **lógica de negocio** y validaciones:

#### Customer (Cliente)

```python
@dataclass
class Customer:
    dni: str          # DNI con formato 12345678A
    name: str         # Nombre del cliente
    surname: str      # Apellidos
    birth_date: date  # Fecha de nacimiento
    email: str        # Email válido
    phone: str        # Teléfono (9-15 dígitos)

    def age(self) -> int:
        """Calcula la edad actual del cliente"""
```

**Validaciones automáticas**:

- DNI: Formato 8 números + 1 letra mayúscula
- Email: Formato estándar de email
- Teléfono: Solo dígitos, entre 9 y 15 caracteres
- Fecha de nacimiento: No puede ser futura

#### Car (Coche)

```python
@dataclass
class Car:
    license_plate: str  # Matrícula única
    brand: str          # Marca del vehículo
    model: str          # Modelo
    year: int           # Año de fabricación
    owner_dni: str      # DNI del propietario
```

#### Appointment (Cita)

```python
@dataclass
class Appointment:
    date: date          # Fecha de la cita
    time: str           # Hora (HH:MM)
    customer_dni: str   # Cliente asociado
    car_license: str    # Coche asociado
    description: str    # Descripción del servicio
    cost: float         # Coste estimado
```

### Servicios de Aplicación (`core/application/`)

Los servicios implementan los **casos de uso** del sistema:

#### Servicios de Cliente

- `RegisterCustomerService`: Registra un nuevo cliente
- `ListCustomerService`: Lista todos los clientes
- `UpdateCustomerService`: Actualiza datos de un cliente
- `DeleteCustomerService`: Elimina un cliente

#### Servicios de Coche

- `RegisterCarService`: Registra un nuevo vehículo
- `ListCarsService`: Lista todos los coches
- `UpdateCarsService`: Actualiza datos de un coche
- `DeleteCarsService`: Elimina un coche

#### Servicios de Citas

- `ScheduleAppointmentService`: Agenda una nueva cita
- `ListAppointmentsByDateService`: Lista citas por fecha
- `UpdateAppointmentService`: Modifica una cita existente
- `DeleteAppointmentService`: Cancela una cita

### Repositorios (`adapters/persistence/`)

Implementan la persistencia en archivos JSON:

- **CustomerJsonRepository**: CRUD de clientes en `data/customers.json`
- **CarJsonRepository**: CRUD de coches en `data/cars.json`
- **AppointmentJsonRepository**: CRUD de citas en `data/appointments.json`

Todos heredan de `JsonBaseRepository` que proporciona operaciones comunes de lectura/escritura.

### Interfaz Gráfica (`adapters/ui/`)

Implementación en Tkinter con diseño moderno:

- **tkinter_main.py**: Ventana principal con pestañas
- **tkinter_forms.py**: Formularios de registro/edición
- **ui_helpers.py**: Utilidades de UI (colores, estilos, widgets)

**Paleta de Colores**:

```python
BG_DARK = "#1a1a2e"        # Fondo principal
BG_CARD = "#16213e"        # Tarjetas/paneles
ACCENT = "#0f3460"         # Acento 1
ACCENT_LIGHT = "#53354a"   # Acento 2
SUCCESS = "#16c79a"        # Verde éxito
WARNING = "#f39c12"        # Naranja advertencia
ERROR = "#e74c3c"          # Rojo error
TEXT_PRIMARY = "#eaeaea"   # Texto principal
TEXT_SECONDARY = "#a0a0a0" # Texto secundario
```

---

## 📸 Capturas de Pantalla

### Pantalla Principal

![Gestión de Clientes](https://via.placeholder.com/800x450/1a1a2e/16c79a?text=Gestión+de+Clientes)

### Gestión de Vehículos

![Gestión de Coches](https://via.placeholder.com/800x450/16213e/f39c12?text=Gestión+de+Vehículos)

### Agenda de Citas

![Agenda de Citas](https://via.placeholder.com/800x450/0f3460/eaeaea?text=Agenda+de+Citas)

---

## 🧪 Testing

### Ejecutar Tests

```bash
python test_forms.py
```

### Estructura de Tests

Los tests verifican:

- ✅ Validaciones del dominio (DNI, email, teléfono)
- ✅ Reglas de negocio (edad, fechas futuras)
- ✅ Funcionamiento de servicios
- ✅ Persistencia JSON

---

## 🛠️ Personalización

### Cambiar Persistencia de JSON a SQLite

Gracias a la arquitectura hexagonal, es fácil cambiar la persistencia:

1. Crear nuevo adaptador `SqliteCustomerRepository` que implemente `CustomerRepositoryProtocol`
2. En `main.py`, reemplazar:
   ```python
   customer_repo = CustomerJsonRepository("data/customers.json")
   # Por:
   customer_repo = SqliteCustomerRepository("data/taller.db")
   ```
3. ¡Sin cambios en dominio ni servicios!

### Cambiar UI de Tkinter a Web

1. Crear adaptador web (Flask/FastAPI)
2. Reutilizar los mismos servicios de aplicación
3. Solo cambiar la capa de UI en `main.py`

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guía de Contribución

- Mantén la arquitectura hexagonal
- Añade tests para nuevas funcionalidades
- Sigue las convenciones de código Python (PEP 8)
- Documenta cambios significativos

---

## 📝 Roadmap

### Próximas Funcionalidades

- [ ] 🔐 Sistema de autenticación de usuarios
- [ ] 📊 Dashboard con estadísticas y métricas
- [ ] 📧 Notificaciones por email de citas próximas
- [ ] 📄 Generación de informes PDF
- [ ] 💾 Soporte para base de datos SQL (PostgreSQL/MySQL)
- [ ] 🌐 API REST para integración con aplicaciones web
- [ ] 📱 Aplicación móvil (React Native/Flutter)
- [ ] 🔔 Sistema de recordatorios automáticos
- [ ] 💳 Integración con sistema de pagos
- [ ] 📅 Vista de calendario mensual

---

## 🐛 Problemas Conocidos

Ninguno en este momento. Si encuentras algún bug, por favor [abre un issue](https://github.com/Dani1lopez/taller_citas_hexagonal/issues).

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Dani López**

- GitHub: [@Dani1lopez](https://github.com/Dani1lopez)
- Proyecto: [taller_citas_hexagonal](https://github.com/Dani1lopez/taller_citas_hexagonal)

---

## 🙏 Agradecimientos

- Inspirado en los principios de **Clean Architecture** de Robert C. Martin
- Basado en **Hexagonal Architecture** de Alistair Cockburn
- Comunidad Python por las excelentes herramientas y librerías

---

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:

1. Revisa la [documentación](#-documentación-técnica)
2. Busca en [issues existentes](https://github.com/Dani1lopez/taller_citas_hexagonal/issues)
3. Crea un [nuevo issue](https://github.com/Dani1lopez/taller_citas_hexagonal/issues/new)

---

<div align="center">

**⭐ Si te ha gustado este proyecto, dale una estrella en GitHub ⭐**

Hecho con ❤️ por Dani López

</div>
