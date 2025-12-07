"""
Script de prueba rápida para debuggear problemas con forms
"""
import flet as ft

def test_customer_form():
    def main(page: ft.Page):
        from adapters.ui.forms import CustomerForm
        from datetime import date
        
        print("🧪 PRUEBA: CustomerForm")
        form = CustomerForm()
        form.set_page(page)
        
        # Llenar el formulario manualmente
        form.dni.value = "12345678A"
        form.name.value = "Juan"
        form.surname.value = "Pérez"
        form.email.value = "juan@test.com"
        form.phone.value = "123456789"
        form.selected_birth_date = date(1990, 1, 1)
        
        # Validar
        print(f"¿Validación correcta? {form.validate()}")
        
        # Obtener datos
        try:
            customer = form.get_data()
            print(f"✅ CLIENTE CREADO: {customer}")
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        page.close()
    
    ft.app(target=main)

def test_car_form():
    def main(page: ft.Page):
        from adapters.ui.forms import CarForm
        from datetime import date
        
        print("\n🧪 PRUEBA: CarForm")
        form = CarForm()
        form.set_page(page)
        
        # Llenar el formulario
        form.plate.value = "1234ABC"
        form.brand.value = "Toyota"
        form.model.value = "Corolla"
        form.year.value = "2020"
        form.last_revision.value = "2024-01-15"
        
        # Validar
        print(f"¿Validación correcta? {form.validate()}")
        
        # Obtener datos
        try:
            car = form.get_data()
            print(f"✅ COCHE CREADO: {car}")
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        page.close()
    
    ft.app(target=main)

if __name__ == "__main__":
    print("=" * 60)
    print("INICIANDO PRUEBAS DE FORMULARIOS")
    print("=" * 60)
    
    test_customer_form()
    test_car_form()
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)
