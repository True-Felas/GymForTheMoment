import customtkinter as ctk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.Model.user_model import UserModel
from Frontend.View.reserv_view import ReservasView

class App(ctk.CTk):
    def __init__(self, usuario_id, usuario_actual):
        super().__init__()

        self.usuario_id = usuario_id
        self.usuario_actual = usuario_actual
        self.user_model = UserModel()
        
        # Definir tamaño de ventana
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 700
        
        self.title(f"Gimnasio - Bienvenido {usuario_actual}")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Centrar ventana
        self.center_window()
        
        # Referencias a las tarjetas para poder actualizarlas
        self.tarjetas = {}
        
        self.crear_interfaz()
        self.actualizar_estadisticas()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        x = (self.winfo_screenwidth() // 2) - (self.WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (self.WINDOW_HEIGHT // 2)
        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}')
    
    def crear_interfaz(self):
        """Crea la interfaz de la aplicación"""
        # ==== Título ====
        titulo = ctk.CTkLabel(self, text="Tus Estadísticas", font=("Arial", 32, "bold"))
        titulo.pack(pady=30)

        # ==== Contenedor de estadísticas ====
        frame_stats = ctk.CTkFrame(self, fg_color="transparent")
        frame_stats.pack(pady=20)

        # Tarjetas de dleratos (guardamos referencias)
        self.tarjetas['reservas'] = self.crear_tarjeta(frame_stats, "Reservas Hechas", "0", "#9333EA", 0, 0)
        self.tarjetas['horas'] = self.crear_tarjeta(frame_stats, "Horas Entrenadas", "0h", "#0EA5E9", 0, 1)
        self.tarjetas['clases'] = self.crear_tarjeta(frame_stats, "Clases Asistidas", "0", "#22C55E", 0, 2)
        self.tarjetas['nivel'] = self.crear_tarjeta(frame_stats, "Progreso", "Nivel 1", "#EF4444", 0, 3)

        # ==== Sección de acciones ====
        acciones = ctk.CTkLabel(self, text="Acciones", font=("Arial", 26, "bold"))
        acciones.pack(pady=(50, 20))

        frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        frame_acciones.pack()

        self.crear_boton_accion(frame_acciones, "Reservar Clase", "#0284C7", 0, 0, self.abrir_reservas)
        self.crear_boton_accion(frame_acciones, "Ver Rutinas", "#16A34A", 0, 1)
        self.crear_boton_accion(frame_acciones, "Ver Progreso", "#DC2626", 1, 0)
        self.crear_boton_accion(frame_acciones, "Historial", "#A855F7", 1, 1)

    # ==== Metodo para crear tarjetas ====
    def crear_tarjeta(self, parent, titulo, valor, color, fila, columna):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=color, width=200, height=140)
        card.grid(row=fila, column=columna, padx=20, pady=15, ipadx=30, ipady=30, sticky="nsew")

        lbl_titulo = ctk.CTkLabel(card, text=titulo, text_color="white", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=(15, 5))
        lbl_valor = ctk.CTkLabel(card, text=valor, text_color="white", font=("Arial", 32, "bold"))
        lbl_valor.pack(pady=(5, 15))
        
        return lbl_valor  # Retornamos la etiqueta del valor para poder actualizarla

    # ==== Metodo para crear botones ====
    def crear_boton_accion(self, parent, texto, color, fila, columna, comando=None):
        btn = ctk.CTkButton(
            parent,
            text=texto,
            fg_color=color,
            hover_color="#1E293B",
            width=220,
            height=100,
            font=("Arial", 20, "bold"),
            command=comando,
            corner_radius=15
        )
        btn.grid(row=fila, column=columna, padx=25, pady=25)
    
    # ==== Actualizar estadísticas desde la base de datos ====
    def actualizar_estadisticas(self):
        """Obtiene y actualiza las estadísticas del usuario"""
        stats = self.user_model.obtener_estadisticas(self.usuario_id)
        
        self.tarjetas['reservas'].configure(text=str(stats['reservas']))
        self.tarjetas['horas'].configure(text=f"{stats['horas']}h")
        self.tarjetas['clases'].configure(text=str(stats['clases']))
        self.tarjetas['nivel'].configure(text=f"Nivel {stats['nivel']}")
    
    # ==== Abrir ventana de reservas ====
    def abrir_reservas(self):
        """Abre la ventana de reservas"""
        ReservasView(self, self.usuario_id, callback_actualizar=self.actualizar_estadisticas)
