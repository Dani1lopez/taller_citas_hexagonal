import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from typing import Optional, List, Dict, Any
import re

from core.domain.customer import Customer
from core.domain.car import Car


# ==========================================
# 🧱 CLASE BASE
# ==========================================
class FormBase(tk.Frame):
    """
    Clase padre de la que heredarán todos los formularios.
    Incluye un label de error global para mostrar errores de dominio/servicio.
    """
    # Enhanced color scheme matching tkinter_main.py
    COLORS = {
        'bg_main': '#0d1117',
        'bg_secondary': '#161b22',
        'bg_card': '#1c2128',
        'text_primary': '#f0f6fc',
        'text_secondary': '#8b949e',
        'text_muted': '#6e7681',
        'success': '#2ea043',
        'success_hover': '#3fb950',
        'danger': '#da3633',
        'danger_hover': '#f85149',
        'primary': '#4493f8',
        'primary_hover': '#539bf5',
        'border': '#30363d',
        'text_on_color': '#ffffff',
    }
    
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=self.COLORS['bg_main'])
        self.configure(padx=20, pady=20)
        
        # Label de error global
        self.global_error_label = tk.Label(
            self,
            text="",
            fg=self.COLORS['danger'],
            bg=self.COLORS['bg_main'],
            font=("Segoe UI", 10, "bold"),
            wraplength=500,
            justify=tk.LEFT
        )
        self.global_error_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
    
    def show_global_error(self, message: str) -> None:
        """Muestra un mensaje de error general."""
        self.global_error_label.config(text=f"⚠️ {message}")
    
    def clear_global_error(self) -> None:
        """Borra el mensaje de error general."""
        self.global_error_label.config(text="")
    
    def validate(self) -> bool:
        """Override en subclases."""
        raise NotImplementedError
    
    def get_data(self):
        """Override en subclases."""
        raise NotImplementedError
    
    def clear(self) -> None:
        """Override en subclases."""
        raise NotImplementedError


# ==========================================
# 📅 COMPONENTE DATEPICKER
# ==========================================
class DatePickerEntry(tk.Frame):
    """
    Componente personalizado para selección de fechas.
    Incluye un Entry de solo lectura y un botón de calendario.
    """
    def __init__(self, parent: tk.Widget, label: str = "Fecha", min_date: Optional[date] = None, max_date: Optional[date] = None) -> None:
        super().__init__(parent)
        
        self.selected_date: Optional[date] = None
        self.min_date = min_date
        self.max_date = max_date
        
        # Entry de solo lectura
        self.entry = tk.Entry(self, width=25, state="readonly")
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón de calendario
        self.btn_calendar = tk.Button(
            self,
            text="📅",
            command=self._open_calendar,
            width=3
        )
        self.btn_calendar.pack(side=tk.LEFT)
        
        # Label de error
        self.error_label = tk.Label(self, text="", fg="red", font=("Helvetica", 9))
        
    def _open_calendar(self) -> None:
        """Abre un diálogo de calendario simple."""
        calendar_window = tk.Toplevel(self)
        calendar_window.title("Seleccionar Fecha")
        calendar_window.geometry("350x380")
        calendar_window.resizable(False, False)
        calendar_window.transient(self.winfo_toplevel())
        calendar_window.grab_set()
        
        # Aplicar colores modernos
        COLORS = FormBase.COLORS
        calendar_window.configure(bg=COLORS['bg_main'])
        
        # Frame principal
        frame = tk.Frame(calendar_window, padx=20, pady=20, bg=COLORS['bg_main'])
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Selector de año
        tk.Label(
            frame,
            text="Año:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['text_primary']
        ).grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        year_var = tk.IntVar(value=date.today().year)
        year_spinbox = tk.Spinbox(
            frame,
            from_=1900,
            to=date.today().year,
            textvariable=year_var,
            width=12,
            font=("Segoe UI", 10),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            buttonbackground=COLORS['bg_card'],
            relief='flat',
            bd=1
        )
        year_spinbox.grid(row=0, column=1, sticky="w", pady=8)
        
        # Selector de mes
        tk.Label(
            frame,
            text="Mes:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['text_primary']
        ).grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
        month_var = tk.IntVar(value=date.today().month)
        month_spinbox = tk.Spinbox(
            frame,
            from_=1,
            to=12,
            textvariable=month_var,
            width=12,
            font=("Segoe UI", 10),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            buttonbackground=COLORS['bg_card'],
            relief='flat',
            bd=1
        )
        month_spinbox.grid(row=1, column=1, sticky="w", pady=8)
        
        # Selector de día
        tk.Label(
            frame,
            text="Día:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_main'],
            fg=COLORS['text_primary']
        ).grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))
        day_var = tk.IntVar(value=date.today().day)
        day_spinbox = tk.Spinbox(
            frame,
            from_=1,
            to=31,
            textvariable=day_var,
            width=12,
            font=("Segoe UI", 10),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            buttonbackground=COLORS['bg_card'],
            relief='flat',
            bd=1
        )
        day_spinbox.grid(row=2, column=1, sticky="w", pady=8)
        
        def set_date():
            try:
                selected = date(year_var.get(), month_var.get(), day_var.get())
                
                # Validar limites
                if self.min_date and selected < self.min_date:
                    messagebox.showerror("Error", f"La fecha no puede ser anterior a {self.min_date}")
                    return
                if self.max_date and selected > self.max_date:
                    messagebox.showerror("Error", f"La fecha no puede ser posterior a {self.max_date}")
                    return
                
                self.selected_date = selected
                self.entry.config(state="normal")
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(selected))
                self.entry.config(state="readonly")
                self.clear_error()
                calendar_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Fecha inválida: {str(e)}")
        
        # Botones con estilo moderno mejorado
        btn_frame = tk.Frame(frame, bg=COLORS['bg_main'])
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Botón Aceptar - Verde profesional mejorado
        btn_accept = tk.Button(
            btn_frame,
            text="Aceptar",
            command=set_date,
            bg=COLORS['success'],  # Verde profesional mejorado
            fg=COLORS['text_on_color'],  # Blanco puro
            font=("Segoe UI", 10, "bold"),
            width=12,
            padx=15,
            pady=8,
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            activebackground=COLORS['success_hover'],
            activeforeground=COLORS['text_on_color'],
            highlightthickness=0
        )
        btn_accept.pack(side=tk.LEFT, padx=5)
        
        # Hover effect para Aceptar
        btn_accept.bind("<Enter>", lambda e: btn_accept.configure(bg=COLORS['success_hover']))
        btn_accept.bind("<Leave>", lambda e: btn_accept.configure(bg=COLORS['success']))
        
        # Botón Cancelar - Gris mejorado
        btn_cancel = tk.Button(
            btn_frame,
            text="Cancelar",
            command=calendar_window.destroy,
            bg='#4a5568',  # Gris medio
            fg=COLORS['text_on_color'],  # Blanco puro
            font=("Segoe UI", 10, "bold"),
            width=12,
            padx=15,
            pady=8,
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            activebackground='#5a6578',
            activeforeground=COLORS['text_on_color'],
            highlightthickness=0
        )
        btn_cancel.pack(side=tk.LEFT, padx=5)
        
        # Hover effect para Cancelar
        btn_cancel.bind("<Enter>", lambda e: btn_cancel.configure(bg='#5a6578'))
        btn_cancel.bind("<Leave>", lambda e: btn_cancel.configure(bg='#4a5568'))
    
    def get_date(self) -> Optional[date]:
        """Obtiene la fecha seleccionada."""
        return self.selected_date
    
    def set_date(self, d: date) -> None:
        """Establece la fecha."""
        self.selected_date = d
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(d))
        self.entry.config(state="readonly")
    
    def set_error(self, message: str) -> None:
        """Muestra mensaje de error."""
        self.error_label.config(text=message)
        self.error_label.pack(side=tk.LEFT, padx=5)
    
    def clear_error(self) -> None:
        """Limpia mensaje de error."""
        self.error_label.config(text="")
        self.error_label.pack_forget()
    
    def clear(self) -> None:
        """Limpia el campo."""
        self.selected_date = None
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.config(state="readonly")
        self.clear_error()


# ==========================================
# 🧑 FORMULARIO DE CLIENTE
# ==========================================
class CustomerForm(FormBase):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        
        current_row = 1
        
        # DNI
        tk.Label(self, text="DNI:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.dni_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.dni_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.dni_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.dni_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Nombre
        tk.Label(self, text="Nombre:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.name_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.name_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.name_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Apellidos
        tk.Label(self, text="Apellidos:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.surname_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.surname_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.surname_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.surname_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Email
        tk.Label(self, text="Email:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.email_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.email_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.email_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Teléfono
        tk.Label(self, text="Teléfono:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.phone_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.phone_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.phone_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.phone_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Fecha de nacimiento
        tk.Label(self, text="Fecha Nacimiento:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.birth_date_picker = DatePickerEntry(
            self,
            min_date=date(1900, 1, 1),
            max_date=date.today()
        )
        self.birth_date_picker.grid(row=current_row, column=1, sticky="w", pady=5)
        current_row += 1
    
    def validate(self) -> bool:
        """Valida visualmente los campos. Retorna True si todo está OK."""
        is_valid = True
        
        # Limpiar errores previos
        self.dni_error.config(text="")
        self.name_error.config(text="")
        self.surname_error.config(text="")
        self.email_error.config(text="")
        self.phone_error.config(text="")
        self.birth_date_picker.clear_error()
        
        # DNI
        dni_val = self.dni_entry.get().strip().upper()
        if not re.match(r"^[0-9]{8}[A-Z]$", dni_val):
            self.dni_error.config(text="Formato: 12345678A")
            is_valid = False
        
        # Nombre
        if not self.name_entry.get().strip():
            self.name_error.config(text="Obligatorio")
            is_valid = False
        
        # Apellidos
        if not self.surname_entry.get().strip():
            self.surname_error.config(text="Obligatorio")
            is_valid = False
        
        # Email
        email_val = self.email_entry.get().strip()
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email_val):
            self.email_error.config(text="Email inválido")
            is_valid = False
        
        # Teléfono
        phone_val = self.phone_entry.get().strip()
        if not phone_val or not phone_val.isdigit() or not (9 <= len(phone_val) <= 15):
            self.phone_error.config(text="9-15 dígitos")
            is_valid = False
        
        # Fecha nacimiento
        if not self.birth_date_picker.get_date():
            self.birth_date_picker.set_error("Obligatorio")
            is_valid = False
        
        if not is_valid:
            self.show_global_error("Revisa los campos marcados en rojo.")
        else:
            self.clear_global_error()
        
        return is_valid
    
    def get_data(self) -> Customer:
        """Devuelve el objeto de dominio. Usar solo si validate() es True."""
        return Customer(
            dni=self.dni_entry.get().strip().upper(),
            name=self.name_entry.get().strip(),
            surname=self.surname_entry.get().strip(),
            email=self.email_entry.get().strip(),
            phone=self.phone_entry.get().strip(),
            birth_date=self.birth_date_picker.get_date(),  # type: ignore
        )
    
    def fill_form(self, customer: Customer) -> None:
        """Rellena el formulario para edición."""
        self.dni_entry.delete(0, tk.END)
        self.dni_entry.insert(0, customer.dni)
        self.dni_entry.config(state="readonly")
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, customer.name)
        
        self.surname_entry.delete(0, tk.END)
        self.surname_entry.insert(0, customer.surname)
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, customer.email)
        
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, customer.phone)
        
        self.birth_date_picker.set_date(customer.birth_date)
        
        self.clear_global_error()
    
    def clear(self) -> None:
        """Limpia el formulario y los errores."""
        self.dni_entry.config(state="normal")
        self.dni_entry.delete(0, tk.END)
        self.dni_error.config(text="")
        
        self.name_entry.delete(0, tk.END)
        self.name_error.config(text="")
        
        self.surname_entry.delete(0, tk.END)
        self.surname_error.config(text="")
        
        self.email_entry.delete(0, tk.END)
        self.email_error.config(text="")
        
        self.phone_entry.delete(0, tk.END)
        self.phone_error.config(text="")
        
        self.birth_date_picker.clear()
        
        self.clear_global_error()


# ==========================================
# 🚗 FORMULARIO DE COCHE
# ==========================================
class CarForm(FormBase):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        
        current_row = 1
        
        # Matrícula
        tk.Label(self, text="Matrícula:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.plate_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.plate_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.plate_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.plate_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Marca
        tk.Label(self, text="Marca:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.brand_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.brand_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.brand_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.brand_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Modelo
        tk.Label(self, text="Modelo:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.model_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.model_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.model_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.model_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Año
        tk.Label(self, text="Año:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.year_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.year_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.year_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.year_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Última revisión (opcional)
        tk.Label(self, text="Última Revisión:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        tk.Label(self, text="(Opcional)", font=("Segoe UI", 8), fg=self.COLORS['text_muted'], bg=self.COLORS['bg_main']).grid(row=current_row, column=0, sticky="w", padx=(105, 0))
        self.last_revision_picker = DatePickerEntry(self)
        self.last_revision_picker.grid(row=current_row, column=1, sticky="w", pady=5)
        current_row += 1
    
    def validate(self) -> bool:
        is_valid = True
        
        # Limpiar errores
        self.plate_error.config(text="")
        self.brand_error.config(text="")
        self.model_error.config(text="")
        self.year_error.config(text="")
        self.last_revision_picker.clear_error()
        
        # Matrícula
        plate_val = self.plate_entry.get().strip().upper()
        if not re.match(r"^[0-9]{4}[A-Z]{3}$", plate_val):
            self.plate_error.config(text="Formato: 1234ABC")
            is_valid = False
        
        # Marca
        if not self.brand_entry.get().strip():
            self.brand_error.config(text="Obligatorio")
            is_valid = False
        
        # Modelo
        if not self.model_entry.get().strip():
            self.model_error.config(text="Obligatorio")
            is_valid = False
        
        # Año
        year_val = self.year_entry.get().strip()
        if not year_val.isdigit():
            self.year_error.config(text="Debe ser un número")
            is_valid = False
        else:
            year_int = int(year_val)
            current_year = date.today().year
            if not (1900 <= year_int <= current_year):
                self.year_error.config(text=f"1900-{current_year}")
                is_valid = False
        
        if not is_valid:
            self.show_global_error("Revisa los campos marcados en rojo.")
        else:
            self.clear_global_error()
        
        return is_valid
    
    def get_data(self) -> Car:
        return Car(
            plate=self.plate_entry.get().strip().upper(),
            brand=self.brand_entry.get().strip(),
            model=self.model_entry.get().strip(),
            year=int(self.year_entry.get()),
            last_revision=self.last_revision_picker.get_date(),
        )
    
    def fill_form(self, car: Car) -> None:
        self.plate_entry.delete(0, tk.END)
        self.plate_entry.insert(0, car.plate)
        self.plate_entry.config(state="readonly")
        
        self.brand_entry.delete(0, tk.END)
        self.brand_entry.insert(0, car.brand)
        
        self.model_entry.delete(0, tk.END)
        self.model_entry.insert(0, car.model)
        
        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, str(car.year))
        
        if car.last_revision:
            self.last_revision_picker.set_date(car.last_revision)
        
        self.clear_global_error()
    
    def clear(self) -> None:
        self.plate_entry.config(state="normal")
        self.plate_entry.delete(0, tk.END)
        self.plate_error.config(text="")
        
        self.brand_entry.delete(0, tk.END)
        self.brand_error.config(text="")
        
        self.model_entry.delete(0, tk.END)
        self.model_error.config(text="")
        
        self.year_entry.delete(0, tk.END)
        self.year_error.config(text="")
        
        self.last_revision_picker.clear()
        
        self.clear_global_error()


# ==========================================
# 📅 FORMULARIO DE CITA
# ==========================================
class AppointmentForm(FormBase):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        
        current_row = 1
        
        # Cliente
        tk.Label(self, text="Cliente:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(self, textvariable=self.customer_var, width=27, state="readonly", font=("Segoe UI", 10))
        self.customer_combo.grid(row=current_row, column=1, sticky="w", pady=5)
        self.customer_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.customer_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Coche
        tk.Label(self, text="Coche:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.car_var = tk.StringVar()
        self.car_combo = ttk.Combobox(self, textvariable=self.car_var, width=27, state="readonly", font=("Segoe UI", 10))
        self.car_combo.grid(row=current_row, column=1, sticky="w", pady=5)
        self.car_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.car_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Fecha
        tk.Label(self, text="Fecha:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.date_picker = DatePickerEntry(self, min_date=date.today())
        self.date_picker.grid(row=current_row, column=1, sticky="w", pady=5)
        current_row += 1
        
        # Hora
        tk.Label(self, text="Hora:", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.hour_var = tk.StringVar()
        self.hour_combo = ttk.Combobox(
            self,
            textvariable=self.hour_var,
            values=[f"{h:02d}:00" for h in range(8, 19)],
            width=27,
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.hour_combo.grid(row=current_row, column=1, sticky="w", pady=5)
        self.hour_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.hour_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Coste
        tk.Label(self, text="Coste (€):", font=("Segoe UI", 10, "bold"), bg=self.COLORS['bg_main'], fg=self.COLORS['text_primary']).grid(row=current_row, column=0, sticky="w", pady=5)
        self.cost_entry = tk.Entry(self, width=30, font=("Segoe UI", 10), bg=self.COLORS['bg_card'], fg=self.COLORS['text_primary'], insertbackground=self.COLORS['text_primary'])
        self.cost_entry.grid(row=current_row, column=1, sticky="w", pady=5)
        self.cost_error = tk.Label(self, text="", fg=self.COLORS['danger'], bg=self.COLORS['bg_main'], font=("Segoe UI", 9))
        self.cost_error.grid(row=current_row, column=2, sticky="w", padx=5)
        current_row += 1
        
        # Diccionarios de mapeo
        self.customer_map: Dict[str, str] = {}  # display -> dni
        self.car_map: Dict[str, str] = {}  # display -> plate
    
    def load_lists(self, customers: List[Customer], cars: List[Car]) -> None:
        """Carga las listas de clientes y coches."""
        # Clientes
        customer_options = []
        self.customer_map = {}
        for c in customers:
            display = f"{c.dni} - {c.name} {c.surname}"
            customer_options.append(display)
            self.customer_map[display] = c.dni
        self.customer_combo['values'] = customer_options
        
        # Coches
        car_options = []
        self.car_map = {}
        for car in cars:
            display = f"{car.plate} - {car.brand} {car.model}"
            car_options.append(display)
            self.car_map[display] = car.plate
        self.car_combo['values'] = car_options
    
    def validate(self) -> bool:
        is_valid = True
        
        # Limpiar errores
        self.customer_error.config(text="")
        self.car_error.config(text="")
        self.date_picker.clear_error()
        self.hour_error.config(text="")
        self.cost_error.config(text="")
        
        # Cliente
        if not self.customer_var.get():
            self.customer_error.config(text="Obligatorio")
            is_valid = False
        
        # Coche
        if not self.car_var.get():
            self.car_error.config(text="Obligatorio")
            is_valid = False
        
        # Fecha
        if not self.date_picker.get_date():
            self.date_picker.set_error("Obligatorio")
            is_valid = False
        
        # Hora
        if not self.hour_var.get():
            self.hour_error.config(text="Obligatorio")
            is_valid = False
        
        # Coste
        try:
            val = float(self.cost_entry.get().strip())
            if val < 0:
                raise ValueError
        except Exception:
            self.cost_error.config(text="Número >= 0")
            is_valid = False
        
        if not is_valid:
            self.show_global_error("Revisa los campos marcados en rojo.")
        else:
            self.clear_global_error()
        
        return is_valid
    
    def get_data(self) -> Dict[str, Any]:
        """Devuelve diccionario para el servicio de citas."""
        t_str = self.hour_var.get()
        t_obj = datetime.strptime(t_str, "%H:%M").time() if t_str else datetime.now().time()
        cost_val = float(self.cost_entry.get().strip())
        
        return {
            "customer_dni": self.customer_map[self.customer_var.get()],
            "car_plate": self.car_map[self.car_var.get()],
            "date_": self.date_picker.get_date(),
            "time_": t_obj,
            "cost": cost_val,
        }
    
    def fill_form(self, appointment: Any) -> None:
        """Rellena el formulario con los datos de una cita existente para edición."""
        # Buscar el display del cliente
        customer_display = None
        for display, dni in self.customer_map.items():
            if dni == appointment.customer.dni:
                customer_display = display
                break
        if customer_display:
            self.customer_var.set(customer_display)
        
        # Buscar el display del coche
        car_display = None
        for display, plate in self.car_map.items():
            if plate == appointment.car.plate:
                car_display = display
                break
        if car_display:
            self.car_var.set(car_display)
        
        # Fecha
        self.date_picker.set_date(appointment.date)
        
        # Hora
        time_str = appointment.time.strftime("%H:%M")
        self.hour_var.set(time_str)
        
        # Coste
        self.cost_entry.delete(0, tk.END)
        self.cost_entry.insert(0, str(appointment.cost))
        
        self.clear_global_error()
    
    def clear(self) -> None:
        self.customer_var.set("")
        self.customer_error.config(text="")
        
        self.car_var.set("")
        self.car_error.config(text="")
        
        self.date_picker.clear()
        
        self.hour_var.set("")
        self.hour_error.config(text="")
        
        self.cost_entry.delete(0, tk.END)
        self.cost_error.config(text="")
        
        self.clear_global_error()
