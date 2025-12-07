import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, List

from adapters.ui.tkinter_forms import CustomerForm, CarForm, AppointmentForm
from core.domain.customer import Customer
from core.domain.car import Car
from core.domain.appointment import Appointment


class MainWindow:
    def __init__(
        self,
        root: tk.Tk,
        # Customer Services
        register_customer: Any,
        list_customers: Any,
        update_customer: Any,
        delete_customer: Any,
        # Car Services
        register_car: Any,
        list_cars: Any,
        update_car: Any,
        delete_car: Any,
        # Appointment Services
        schedule_appointment: Any,
        list_appointments: Any,
        update_appointment: Any,
        delete_appointment: Any,
    ) -> None:
        self.root = root
        
        # Servicios clientes
        self.reg_cust = register_customer
        self.list_cust = list_customers
        self.upd_cust = update_customer
        self.del_cust = delete_customer
        
        # Servicios coches
        self.reg_car = register_car
        self.list_car = list_cars
        self.upd_car = update_car
        self.del_car = delete_car
        
        # Servicios citas
        self.sched_appt = schedule_appointment
        self.list_appt = list_appointments
        self.upd_appt = update_appointment
        self.del_appt = delete_appointment
        
        # =======================================
        # ENHANCED MODERN COLOR PALETTE
        # =======================================
        self.COLORS = {
            # Backgrounds - Darker, more sophisticated
            'bg_main': '#0d1117',           # Deep dark background (GitHub-inspired)
            'bg_secondary': '#161b22',      # Secondary panel background
            'bg_card': '#1c2128',           # Card/panel background
            'bg_hover': '#21262d',          # Hover state
            'bg_dialog': '#0d1117',         # Dialog background
            
            # Accents - Enhanced vibrant colors for better contrast
            'primary': '#4493f8',           # Brighter professional blue
            'primary_hover': '#539bf5',     # Primary hover state
            'success': '#2ea043',           # More saturated green
            'success_hover': '#3fb950',     # Success hover state
            'warning': '#e3b341',           # Brighter warm orange
            'warning_hover': '#f0c452',     # Warning hover state
            'danger': '#da3633',            # More intense red
            'danger_hover': '#f85149',      # Danger hover state
            'info': '#8957e5',              # More vibrant purple
            'info_hover': '#a371f7',        # Info hover state
            
            # Text - Better contrast
            'text_primary': '#f0f6fc',      # Very light gray-white
            'text_secondary': '#8b949e',    # Medium gray
            'text_muted': '#6e7681',        # Muted gray
            'text_on_color': '#ffffff',     # Pure white for buttons
            
            # UI Elements
            'border': '#30363d',            # Border color
            'table_header': '#21262d',      # Table header background
            'table_odd': '#161b22',         # Table odd rows
            'table_even': '#0d1117',        # Table even rows
            'table_select': '#1f6feb',      # Brighter table selection
            'input_bg': '#0d1117',          # Input background
            'input_border': '#30363d',      # Input border
        }
        
        # Configuración de la ventana
        self.root.title("🚗 Sistema Taller - Gestión Profesional")
        self.root.geometry("1400x800")
        self.root.configure(bg=self.COLORS['bg_main'])
        
        # Configure ttk styles
        self._configure_styles()
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.COLORS['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Enhanced header with better spacing
        title_frame = tk.Frame(main_container, bg=self.COLORS['bg_secondary'], height=95)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        title_frame.pack_propagate(False)
        
        # Inner container for proper vertical centering
        title_inner = tk.Frame(title_frame, bg=self.COLORS['bg_secondary'])
        title_inner.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(
            title_inner,
            text="🚗 SISTEMA DE GESTIÓN DE TALLER",
            font=("Segoe UI", 24, "bold"),
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['primary']
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(
            title_inner,
            text="Arquitectura Hexagonal | Gestión Profesional de Clientes, Vehículos y Citas",
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_secondary']
        )
        subtitle_label.pack()
        
        # Crear notebook (tabs)
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear tabs
        self._build_customers_tab()
        self._build_cars_tab()
        self._build_appointments_tab()
        
        # Cargar datos iniciales
        self._refresh_cust_table()
        self._refresh_car_table()
        self._refresh_appt_table()
    
    def _configure_styles(self) -> None:
        """Configure modern ttk styles."""
        style = ttk.Style()
        
        # Notebook style
        style.theme_use('default')
        style.configure('Modern.TNotebook', 
                       background=self.COLORS['bg_main'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_secondary'],
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'))
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.COLORS['bg_secondary'])],
                 foreground=[('selected', self.COLORS['primary'])])
        
        # Treeview (table) style
        style.configure('Modern.Treeview',
                       background=self.COLORS['table_even'],
                       foreground=self.COLORS['text_primary'],
                       fieldbackground=self.COLORS['table_even'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       rowheight=35)
        style.configure('Modern.Treeview.Heading',
                       background=self.COLORS['table_header'],
                       foreground=self.COLORS['text_primary'],
                       borderwidth=1,
                       relief='flat',
                       font=('Segoe UI', 11, 'bold'))
        style.map('Modern.Treeview',
                 background=[('selected', self.COLORS['table_select'])],
                 foreground=[('selected', self.COLORS['bg_main'])])
        
        # Combobox style
        style.configure('Modern.TCombobox',
                       fieldbackground=self.COLORS['bg_card'],
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_primary'],
                       borderwidth=1,
                       relief='flat')
        
        # Scrollbar style  
        style.configure('Modern.Vertical.TScrollbar',
                       background=self.COLORS['bg_card'],
                       troughcolor=self.COLORS['bg_secondary'],
                       borderwidth=0,
                       arrowcolor=self.COLORS['primary'])
    
    # ==========================
    # CUSTOMER LOGIC
    # ==========================
    def _build_customers_tab(self) -> None:
        """Construye el tab de clientes."""
        tab = tk.Frame(self.notebook, bg=self.COLORS['bg_main'])
        self.notebook.add(tab, text="👥 Clientes")
        
        # Header
        header = tk.Frame(tab, bg=self.COLORS['bg_secondary'], height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        header_inner = tk.Frame(header, bg=self.COLORS['bg_secondary'])
        header_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        tk.Label(
            header_inner,
            text="Gestión de Clientes",
            font=("Segoe UI", 18, "bold"),
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_primary']
        ).pack(side=tk.LEFT)
        
        self._create_modern_button(
            header_inner,
            text="➕ Nuevo Cliente",
            command=self._open_new_cust_dialog,
            bg=self.COLORS['success'],
            side=tk.RIGHT
        )
        
        # Tabla
        table_frame = tk.Frame(tab, bg=self.COLORS['bg_main'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, style='Modern.Vertical.TScrollbar')
        
        # Treeview
        self.cust_table = ttk.Treeview(
            table_frame,
            columns=("DNI", "Nombre", "Email", "Edad", "Teléfono"),
            show="headings",
            yscrollcommand=scroll_y.set,
            style='Modern.Treeview'
        )
        
        scroll_y.config(command=self.cust_table.yview)
        
        # Configurar columnas
        self.cust_table.heading("DNI", text="DNI")
        self.cust_table.heading("Nombre", text="Nombre Completo")
        self.cust_table.heading("Email", text="Email")
        self.cust_table.heading("Edad", text="Edad")
        self.cust_table.heading("Teléfono", text="Teléfono")
        
        self.cust_table.column("DNI", width=100)
        self.cust_table.column("Nombre", width=200)
        self.cust_table.column("Email", width=250)
        self.cust_table.column("Edad", width=80)
        self.cust_table.column("Teléfono", width=150)
        
        # Layout
        self.cust_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        actions_frame = tk.Frame(tab, bg=self.COLORS['bg_main'])
        actions_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_modern_button(
            actions_frame,
            text="✏️ Editar",
            command=self._edit_selected_customer,
            bg=self.COLORS['info'],
            side=tk.LEFT,
            padx=5
        )
        
        self._create_modern_button(
            actions_frame,
            text="🗑️ Eliminar",
            command=self._delete_selected_customer,
            bg=self.COLORS['danger'],
            side=tk.LEFT,
            padx=5
        )
    
    def _create_modern_button(self, parent, text, command, bg, side=tk.LEFT, padx=0):
        """Helper para crear botones modernos con estilo consistente y máximo contraste."""
        # Determinar color hover basado en el color base
        hover_color = None
        if bg == self.COLORS['success']:
            hover_color = self.COLORS['success_hover']
        elif bg == self.COLORS['danger']:
            hover_color = self.COLORS['danger_hover']
        elif bg == self.COLORS['info']:
            hover_color = self.COLORS['info_hover']
        elif bg == self.COLORS['primary']:
            hover_color = self.COLORS['primary_hover']
        elif bg == self.COLORS['warning']:
            hover_color = self.COLORS['warning_hover']
        else:
            hover_color = self._lighten_color(bg)
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=self.COLORS['text_on_color'],  # Siempre blanco puro para máximo contraste
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            activebackground=hover_color,
            activeforeground=self.COLORS['text_on_color'],
            highlightthickness=0
        )
        btn.pack(side=side, padx=padx)
        
        # Hover effect mejorado
        def on_enter(e):
            btn.configure(background=hover_color)
        
        def on_leave(e):
            btn.configure(background=bg)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def _lighten_color(self, hex_color):
        """Clarear un color hex para el efecto hover."""
        # Simple lightening by adding 0x20 to each component
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 32)
        g = min(255, g + 32)
        b = min(255, b + 32)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _create_dialog_button(self, parent, text, command, style='primary', width=12):
        """Helper para crear botones modernos en diálogos con máximo contraste.
        
        Args:
            parent: Widget padre
            text: Texto del botón
            command: Función a ejecutar
            style: 'primary' (guardar), 'secondary' (cancelar), 'danger' (eliminar)
            width: Ancho del botón
        """
        # Configuración de colores mejorados para cada estilo
        if style == 'primary':
            bg_color = self.COLORS['success']
            hover_color = self.COLORS['success_hover']
        elif style == 'secondary':
            bg_color = '#4a5568'  # Gris medio
            hover_color = '#5a6578'
        elif style == 'danger':
            bg_color = self.COLORS['danger']
            hover_color = self.COLORS['danger_hover']
        else:
            bg_color = self.COLORS['primary']
            hover_color = self.COLORS['primary_hover']
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=self.COLORS['text_on_color'],  # Blanco puro para máximo contraste
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            borderwidth=0,
            relief='flat',
            cursor='hand2',
            width=width,
            activebackground=hover_color,
            activeforeground=self.COLORS['text_on_color'],
            highlightthickness=0
        )
        
        # Hover effect mejorado
        def on_enter(e):
            btn.configure(background=hover_color)
        
        def on_leave(e):
            btn.configure(background=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def _refresh_cust_table(self) -> None:
        """Refresca la tabla de clientes."""
        # Limpiar
        for item in self.cust_table.get_children():
            self.cust_table.delete(item)
        
        # Cargar datos
        customers: List[Customer] = self.list_cust.execute()
        for c in customers:
            self.cust_table.insert(
                "",
                tk.END,
                values=(c.dni, f"{c.name} {c.surname}", c.email, c.age(), c.phone),
                tags=(c.dni,)
            )
    
    def _open_new_cust_dialog(self) -> None:
        """Abre diálogo para nuevo cliente."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Cliente")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.COLORS['bg_dialog'])
        
        form = CustomerForm(dialog)
        form.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        btn_frame = tk.Frame(dialog, bg=self.COLORS['bg_dialog'])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def save():
            if not form.validate():
                return
            try:
                data = form.get_data()
                self.reg_cust.execute(data)
                messagebox.showinfo("Éxito", "Cliente registrado correctamente")
                dialog.destroy()
                self._refresh_cust_table()
            except Exception as ex:
                form.show_global_error(str(ex))
        
        self._create_dialog_button(btn_frame, "Guardar", save, style='primary').pack(side=tk.RIGHT, padx=5)
        self._create_dialog_button(btn_frame, "Cancelar", dialog.destroy, style='secondary').pack(side=tk.RIGHT, padx=5)
    
    def _edit_selected_customer(self) -> None:
        """Edita el cliente seleccionado."""
        selection = self.cust_table.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero")
            return
        
        item = selection[0]
        dni = self.cust_table.item(item)["tags"][0]
        
        # Buscar cliente
        customers = self.list_cust.execute()
        customer = next((c for c in customers if c.dni == dni), None)
        if not customer:
            return
        
        # Abrir diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Cliente")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.COLORS['bg_dialog'])
        
        form = CustomerForm(dialog)
        form.fill_form(customer)
        form.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        btn_frame = tk.Frame(dialog, bg=self.COLORS['bg_dialog'])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def save():
            if not form.validate():
                return
            try:
                data = form.get_data()
                self.upd_cust.execute(data)
                messagebox.showinfo("Éxito", "Cliente actualizado")
                dialog.destroy()
                self._refresh_cust_table()
            except Exception as ex:
                form.show_global_error(str(ex))
        
        self._create_dialog_button(btn_frame, "Guardar", save, style='primary').pack(side=tk.RIGHT, padx=5)
        self._create_dialog_button(btn_frame, "Cancelar", dialog.destroy, style='secondary').pack(side=tk.RIGHT, padx=5)
    
    def _delete_selected_customer(self) -> None:
        """Elimina el cliente seleccionado."""
        selection = self.cust_table.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero")
            return
        
        item = selection[0]
        dni = self.cust_table.item(item)["tags"][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar cliente {dni}?"):
            try:
                self.del_cust.execute(dni)
                messagebox.showinfo("Éxito", "Cliente eliminado")
                self._refresh_cust_table()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))
    
    # ==========================
    # CAR LOGIC
    # ==========================
    def _build_cars_tab(self) -> None:
        """Construye el tab de coches."""
        tab = tk.Frame(self.notebook, bg=self.COLORS['bg_main'])
        self.notebook.add(tab, text="🚗 Coches")
        
        # Header
        header = tk.Frame(tab, bg=self.COLORS['bg_secondary'], height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        header_inner = tk.Frame(header, bg=self.COLORS['bg_secondary'])
        header_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        tk.Label(
            header_inner,
            text="Gestión de Vehículos",
            font=("Segoe UI", 18, "bold"),
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_primary']
        ).pack(side=tk.LEFT)
        
        self._create_modern_button(
            header_inner,
            text="➕ Nuevo Coche",
            command=self._open_new_car_dialog,
            bg=self.COLORS['success'],
            side=tk.RIGHT
        )
        
        # Tabla
        table_frame = tk.Frame(tab, bg=self.COLORS['bg_main'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, style='Modern.Vertical.TScrollbar')
        
        self.car_table = ttk.Treeview(
            table_frame,
            columns=("Matrícula", "Marca/Modelo", "Año", "Revisión"),
            show="headings",
            yscrollcommand=scroll_y.set,
            style='Modern.Treeview'
        )
        
        scroll_y.config(command=self.car_table.yview)
        
        self.car_table.heading("Matrícula", text="Matrícula")
        self.car_table.heading("Marca/Modelo", text="Marca/Modelo")
        self.car_table.heading("Año", text="Año")
        self.car_table.heading("Revisión", text="Necesita Revisión")
        
        self.car_table.column("Matrícula", width=120)
        self.car_table.column("Marca/Modelo", width=300)
        self.car_table.column("Año", width=100)
        self.car_table.column("Revisión", width=150)
        
        self.car_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        actions_frame = tk.Frame(tab, bg=self.COLORS['bg_main'])
        actions_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_modern_button(
            actions_frame,
            text="✏️ Editar",
            command=self._edit_selected_car,
            bg=self.COLORS['info'],
            side=tk.LEFT,
            padx=5
        )
        
        self._create_modern_button(
            actions_frame,
            text="🗑️ Eliminar",
            command=self._delete_selected_car,
            bg=self.COLORS['danger'],
            side=tk.LEFT,
            padx=5
        )
    
    def _refresh_car_table(self) -> None:
        """Refresca la tabla de coches."""
        for item in self.car_table.get_children():
            self.car_table.delete(item)
        
        cars: List[Car] = self.list_car.execute()
        for c in cars:
            needs_rev = "⚠️ SÍ" if c.needs_revision() else "✅ NO"
            self.car_table.insert(
                "",
                tk.END,
                values=(c.plate, f"{c.brand} {c.model}", c.year, needs_rev),
                tags=(c.plate,)
            )
    
    def _open_new_car_dialog(self) -> None:
        """Abre diálogo para nuevo coche."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuevo Coche")
        dialog.geometry("600x450")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.COLORS['bg_dialog'])
        
        form = CarForm(dialog)
        form.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['bg_dialog'])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def save():
            if not form.validate():
                return
            try:
                data = form.get_data()
                self.reg_car.execute(data)
                messagebox.showinfo("Éxito", "Coche registrado")
                dialog.destroy()
                self._refresh_car_table()
            except Exception as ex:
                form.show_global_error(str(ex))
        
        self._create_dialog_button(btn_frame, "Guardar", save, style='primary').pack(side=tk.RIGHT, padx=5)
        self._create_dialog_button(btn_frame, "Cancelar", dialog.destroy, style='secondary').pack(side=tk.RIGHT, padx=5)
    
    def _edit_selected_car(self) -> None:
        """Edita el coche seleccionado."""
        selection = self.car_table.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un coche primero")
            return
        
        item = selection[0]
        plate = self.car_table.item(item)["tags"][0]
        
        cars = self.list_car.execute()
        car = next((c for c in cars if c.plate == plate), None)
        if not car:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Coche")
        dialog.geometry("600x450")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.COLORS['bg_dialog'])
        
        form = CarForm(dialog)
        form.fill_form(car)
        form.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['bg_dialog'])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def save():
            if not form.validate():
                return
            try:
                data = form.get_data()
                self.upd_car.execute(data)
                messagebox.showinfo("Éxito", "Coche actualizado")
                dialog.destroy()
                self._refresh_car_table()
            except Exception as ex:
                form.show_global_error(str(ex))
        
        self._create_dialog_button(btn_frame, "Guardar", save, style='primary').pack(side=tk.RIGHT, padx=5)
        self._create_dialog_button(btn_frame, "Cancelar", dialog.destroy, style='secondary').pack(side=tk.RIGHT, padx=5)
    
    def _delete_selected_car(self) -> None:
        """Elimina el coche seleccionado."""
        selection = self.car_table.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un coche primero")
            return
        
        item = selection[0]
        plate = self.car_table.item(item)["tags"][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar coche {plate}?"):
            try:
                self.del_car.execute(plate)
                messagebox.showinfo("Éxito", "Coche eliminado")
                self._refresh_car_table()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))
    
    # ==========================
    # APPOINTMENT LOGIC
    # ==========================
    def _build_appointments_tab(self) -> None:
        """Construye el tab de citas."""
        tab = tk.Frame(self.notebook, bg=self.COLORS['bg_main'])
        self.notebook.add(tab, text="📅 Citas")
        
        # Header
        header = tk.Frame(tab, bg=self.COLORS['bg_secondary'], height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        header_inner = tk.Frame(header, bg=self.COLORS['bg_secondary'])
        header_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        tk.Label(
            header_inner,
            text="Gestión de Citas",
            font=("Segoe UI", 18, "bold"),
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_primary']
        ).pack(side=tk.LEFT)
        
        self._create_modern_button(
            header_inner,
            text="➕ Agendar Cita",
            command=self._open_new_appt_dialog,
            bg=self.COLORS['success'],
            side=tk.RIGHT
        )
        
        # Info
        info_frame = tk.Frame(tab, bg=self.COLORS['bg_main'])
        info_frame.pack(fill=tk.X, padx=20, pady=(10, 5))
        tk.Label(
            info_frame,
            text="📊 Mostrando todas las citas (ordenadas por fecha)",
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_main'],
            fg=self.COLORS['text_secondary']
        ).pack(side=tk.LEFT)
        
        # Tabla
        table_frame = tk.Frame(tab, bg=self.COLORS['bg_main'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, style='Modern.Vertical.TScrollbar')
        
        self.appt_table = ttk.Treeview(
            table_frame,
            columns=("Fecha", "Hora", "Cliente", "Coche", "Coste"),
            show="headings",
            yscrollcommand=scroll_y.set,
            style='Modern.Treeview'
        )
        
        scroll_y.config(command=self.appt_table.yview)
        
        self.appt_table.heading("Fecha", text="Fecha")
        self.appt_table.heading("Hora", text="Hora")
        self.appt_table.heading("Cliente", text="Cliente (DNI)")
        self.appt_table.heading("Coche", text="Coche (Matrícula)")
        self.appt_table.heading("Coste", text="Coste (€)")
        
        self.appt_table.column("Fecha", width=120)
        self.appt_table.column("Hora", width=100)
        self.appt_table.column("Cliente", width=200)
        self.appt_table.column("Coche", width=200)
        self.appt_table.column("Coste", width=100)
        
        self.appt_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        actions_frame = tk.Frame(tab, bg=self.COLORS['bg_main'])
        actions_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._create_modern_button(
            actions_frame,
            text="✏️ Editar",
            command=self._edit_selected_appt,
            bg=self.COLORS['info'],
            side=tk.LEFT,
            padx=5
        )
        
        self._create_modern_button(
            actions_frame,
            text="🗑️ Cancelar Cita",
            command=self._delete_selected_appt,
            bg=self.COLORS['danger'],
            side=tk.LEFT,
            padx=5
        )
    
    def _refresh_appt_table(self) -> None:
        """Refresca la tabla de citas (muestra todas las citas ordenadas)."""
        for item in self.appt_table.get_children():
            self.appt_table.delete(item)
        
        # Obtener todas las citas desde el repositorio
        all_appts: List[Appointment] = self.list_appt.execute()
        
        # Ordenarlas por fecha y hora
        sorted_appts = sorted(all_appts, key=lambda a: (a.date, a.time))
        
        for idx, a in enumerate(sorted_appts):
            self.appt_table.insert(
                "",
                tk.END,
                values=(
                    str(a.date),
                    a.time.strftime("%H:%M"),
                    a.customer.dni,
                    a.car.plate,
                    f"{a.cost} €"
                ),
                tags=(str(idx),)
            )
        
        # Guardar referencia temporal para eliminar
        self._current_appointments = sorted_appts
    
    def _open_new_appt_dialog(self) -> None:
        """Abre diálogo para nueva cita."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Agendar Cita")
        dialog.geometry("600x450")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.COLORS['bg_dialog'])
        
        form = AppointmentForm(dialog)
        
        # Cargar listas
        custs: List[Customer] = self.list_cust.execute()
        cars: List[Car] = self.list_car.execute()
        form.load_lists(custs, cars)
        
        form.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['bg_dialog'])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def save():
            if not form.validate():
                return
            try:
                data = form.get_data()
                self.sched_appt.execute(**data)
                messagebox.showinfo("Éxito", "Cita agendada correctamente")
                dialog.destroy()
                self._refresh_appt_table()
            except Exception as ex:
                form.show_global_error(str(ex))
        
        self._create_dialog_button(btn_frame, "Guardar", save, style='primary').pack(side=tk.RIGHT, padx=5)
        self._create_dialog_button(btn_frame, "Cancelar", dialog.destroy, style='secondary').pack(side=tk.RIGHT, padx=5)
    
    def _edit_selected_appt(self) -> None:
        """Edita la cita seleccionada."""
        selection = self.appt_table.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una cita primero")
            return
        
        item = selection[0]
        idx = int(self.appt_table.item(item)["tags"][0])
        original_appt = self._current_appointments[idx]
        
        # Abrir diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Cita")
        dialog.geometry("600x450")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.COLORS['bg_dialog'])
        
        form = AppointmentForm(dialog)
        
        # Cargar listas de clientes y coches
        custs: List[Customer] = self.list_cust.execute()
        cars: List[Car] = self.list_car.execute()
        form.load_lists(custs, cars)
        
        # Rellenar el formulario con los datos actuales
        form.fill_form(original_appt)
        
        form.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['bg_dialog'])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def save():
            if not form.validate():
                return
            try:
                data = form.get_data()
                
                # Primero eliminamos la cita original
                self.del_appt.execute(original_appt)
                # Luego creamos la nueva cita actualizada
                self.sched_appt.execute(
                    customer_dni=data["customer_dni"],
                    car_plate=data["car_plate"],
                    date_=data["date_"],
                    time_=data["time_"],
                    cost=data["cost"]
                )
                
                messagebox.showinfo("Éxito", "Cita actualizada correctamente")
                dialog.destroy()
                self._refresh_appt_table()
            except Exception as ex:
                form.show_global_error(str(ex))
        
        self._create_dialog_button(btn_frame, "Guardar", save, style='primary').pack(side=tk.RIGHT, padx=5)
        self._create_dialog_button(btn_frame, "Cancelar", dialog.destroy, style='secondary').pack(side=tk.RIGHT, padx=5)
    
    def _delete_selected_appt(self) -> None:
        """Elimina la cita seleccionada."""
        selection = self.appt_table.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una cita primero")
            return
        
        item = selection[0]
        idx = int(self.appt_table.item(item)["tags"][0])
        appt = self._current_appointments[idx]
        
        if messagebox.askyesno("Confirmar", f"¿Cancelar cita del {appt.date} a las {appt.time.strftime('%H:%M')}?"):
            try:
                self.del_appt.execute(appt)
                messagebox.showinfo("Éxito", "Cita cancelada")
                self._refresh_appt_table()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))
