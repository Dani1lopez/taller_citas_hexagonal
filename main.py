import os
import tkinter as tk

# --- 1. IMPORTAMOS LOS ADAPTADORES (Repositorios) ---
from adapters.persistence.car_json_repository import CarJsonRepository
from adapters.persistence.customer_json_repository import CustomerJsonRepository
from adapters.persistence.appointment_json_repository import AppointmentJsonRepository

# --- 2. IMPORTAMOS LOS SERVICIOS ---
# Servicios de Cliente
from core.application.customer_services import (
    RegisterCustomerService,
    ListCustomerService,
    UpdateCustomerService,
    DeleteCustomerService,
)

# Servicios de Coche
from core.application.car_services import (
    RegisterCarService,
    ListCarsService,
    UpdateCarsService,
    DeleteCarsService,
)

# Servicios de Cita
from core.application.appointment_services import (
    SheduleAppointmentService,
    ListAppointmentsByDateService,
    UpdateAppointmentService,
    DeleteAppointmentService,
)

# --- 3. IMPORTAMOS LA INTERFAZ GRÁFICA ---
from adapters.ui.tkinter_main import MainWindow


def main():
    print("🚗 INICIANDO SISTEMA TALLER (Arquitectura Hexagonal + tkinter)...")

    # --- PASO A: CONFIGURACIÓN (INFRAESTRUCTURA) ---
    # Creamos la carpeta de datos si no existe
    if not os.path.exists("data"):
        os.makedirs("data")

    # Instanciamos los Repositorios
    car_repo = CarJsonRepository("data/cars.json")
    customer_repo = CustomerJsonRepository("data/customers.json")
    appointment_repo = AppointmentJsonRepository(
        "data/appointments.json", customer_repo, car_repo
    )

    # --- PASO B: INYECCIÓN (CABLEADO) ---
    # Le damos los repositorios a los Servicios.
    # Los servicios NO saben que es JSON, solo ven el "Protocolo".

    # Servicios de Cliente
    register_customer = RegisterCustomerService(customer_repo)
    list_customers = ListCustomerService(customer_repo)
    update_customer = UpdateCustomerService(customer_repo)
    delete_customer = DeleteCustomerService(customer_repo)

    # Servicios de Coche
    register_car = RegisterCarService(car_repo)
    list_cars = ListCarsService(car_repo)
    update_car = UpdateCarsService(car_repo)
    delete_car = DeleteCarsService(car_repo)

    # Servicios de Cita
    schedule_appointment = SheduleAppointmentService(
        appointment_repo, customer_repo, car_repo
    )
    list_appointments = ListAppointmentsByDateService(appointment_repo)
    update_appointment = UpdateAppointmentService(appointment_repo)
    delete_appointment = DeleteAppointmentService(appointment_repo)

    # --- PASO C: CREACIÓN DE LA INTERFAZ (UI) ---
    # Creamos la ventana tkinter
    root = tk.Tk()
    
    # Instanciamos la ventana principal y le pasamos TODOS los servicios
    app = MainWindow(
        root,
        # Customer Services
        register_customer=register_customer,
        list_customers=list_customers,
        update_customer=update_customer,
        delete_customer=delete_customer,
        # Car Services
        register_car=register_car,
        list_cars=list_cars,
        update_car=update_car,
        delete_car=delete_car,
        # Appointment Services
        schedule_appointment=schedule_appointment,
        list_appointments=list_appointments,
        update_appointment=update_appointment,
        delete_appointment=delete_appointment,
    )

    # --- PASO D: LANZAR LA APLICACIÓN TKINTER ---
    print("✅ Lanzando interfaz gráfica tkinter...")
    root.mainloop()


if __name__ == "__main__":
    main()