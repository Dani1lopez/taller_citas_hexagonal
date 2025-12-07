import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_modern_tab(parent_frame, colors: dict, title: str, columns: Tuple, 
                     table_widths: dict, add_command, edit_command, delete_command) -> Tuple:
    """Helper para crear tabs modernos con estructura consistente."""
    
    # Header
    header = tk.Frame(parent_frame, bg=colors['bg_secondary'], height=60)
    header.pack(fill=tk.X, padx=0, pady=0)
    header.pack_propagate(False)
    
    header_inner = tk.Frame(header, bg=colors['bg_secondary'])
    header_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
    
    tk.Label(
        header_inner,
        text=title,
        font=("Segoe UI", 18, "bold"),
        bg=colors['bg_secondary'],
        fg=colors['text_primary']
    ).pack(side=tk.LEFT)
    
    # Botón agregar se retorna para ser configurado
    add_btn_frame = tk.Frame(header_inner, bg=colors['bg_secondary'])
    add_btn_frame.pack(side=tk.RIGHT)
    
    # Tabla
    table_frame = tk.Frame(parent_frame, bg=colors['bg_main'])
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
    
    # Scrollbar
    scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, style='Modern.Vertical.TScrollbar')
    
    # Treeview
    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=scroll_y.set,
        style='Modern.Treeview'
    )
    
    scroll_y.config(command=table.yview)
    
    # Configurar columnas
    for col in columns:
        table.heading(col, text=col)
        if col in table_widths:
            table.column(col, width=table_widths[col])
    
    # Layout
    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Botones de acción
    actions_frame = tk.Frame(parent_frame, bg=colors['bg_main'])
    actions_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
    
    return table, add_btn_frame, actions_frame
