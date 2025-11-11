import customtkinter as ctk
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.Model.reserv_model import ReservaModel


class HistorialView(ctk.CTkToplevel):
    def __init__(self, parent, usuario_id):
        super().__init__(parent)

        self.usuario_id = usuario_id
        
        self.title("📜 Historial de Reservas")
        self.geometry("900x700")
        self.resizable(True, True)

        # Centrar el diálogo
        self.center_window()

        # Hacer que la ventana sea modal
        self.transient(parent)
        self.grab_set()

        self.crear_interfaz()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = 900
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        """Crea la interfaz del historial"""
        # Título
        ctk.CTkLabel(
            self,
            text="Historial de Reservas",
            font=("Arial", 36, "bold")
        ).pack(pady=20)

        # Subtítulo
        ctk.CTkLabel(
            self,
            text="Todas tus reservas completadas",
            font=("Arial", 16),
            text_color="gray"
        ).pack(pady=(0, 20))

        # Frame para filtros
        filtros_frame = ctk.CTkFrame(self, fg_color="transparent")
        filtros_frame.pack(pady=10)

        ctk.CTkLabel(
            filtros_frame,
            text="Filtrar por:",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)

        self.filtro_var = ctk.StringVar(value="todas")
        
        ctk.CTkRadioButton(
            filtros_frame,
            text="Todas",
            variable=self.filtro_var,
            value="todas",
            command=self.actualizar_historial
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            filtros_frame,
            text="Completadas",
            variable=self.filtro_var,
            value="completadas",
            command=self.actualizar_historial
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            filtros_frame,
            text="Pendientes",
            variable=self.filtro_var,
            value="pendientes",
            command=self.actualizar_historial
        ).pack(side="left", padx=5)

        # Frame scrollable para el historial
        self.historial_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.historial_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Cargar historial
        self.actualizar_historial()

        # Botón cerrar
        ctk.CTkButton(
            self,
            text="Cerrar",
            command=self.destroy,
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C"
        ).pack(pady=20)

    def actualizar_historial(self):
        """Actualiza la lista de reservas"""
        # Limpiar frame
        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        # Obtener reservas del usuario
        reserva_model = ReservaModel()
        reservas = reserva_model.obtener_reservas_usuario(self.usuario_id)

        # Filtrar según selección
        filtro = self.filtro_var.get()
        if filtro == "completadas":
            reservas = [r for r in reservas if r[5] == 1]  # completada = 1
        elif filtro == "pendientes":
            reservas = [r for r in reservas if r[5] == 0]  # completada = 0

        if not reservas:
            ctk.CTkLabel(
                self.historial_frame,
                text="No hay reservas para mostrar",
                font=("Arial", 18),
                text_color="gray"
            ).pack(pady=50)
            return

        # Mostrar estadísticas generales
        total_reservas = len(reservas)
        completadas = sum(1 for r in reservas if r[5] == 1)
        pendientes = total_reservas - completadas

        stats_frame = ctk.CTkFrame(self.historial_frame, corner_radius=10)
        stats_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(
            stats_frame,
            text=f"Resumen: {total_reservas} reservas totales | {completadas} completadas | {pendientes} pendientes",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        # Mostrar cada reserva
        for reserva in reservas:
            reserva_id, maquina, fecha, hora, duracion, completada = reserva
            
            self.crear_tarjeta_reserva(
                maquina, fecha, hora, duracion, completada
            )

    def crear_tarjeta_reserva(self, maquina, fecha, hora, duracion, completada):
        """Crea una tarjeta para mostrar una reserva"""
        # Determinar color según estado
        if completada:
            color_border = "#22C55E"
            icono = "[OK]"
            estado_texto = "COMPLETADA"
            color_estado = "#22C55E"
        else:
            color_border = "#EAB308"
            icono = "[...]"
            estado_texto = "PENDIENTE"
            color_estado = "#EAB308"

        # Frame de la tarjeta
        tarjeta = ctk.CTkFrame(
            self.historial_frame,
            corner_radius=10,
            border_width=2,
            border_color=color_border,
            fg_color="#1a1a1a"
        )
        tarjeta.pack(pady=8, padx=10, fill="x")

        # Container principal horizontal
        main_container = ctk.CTkFrame(tarjeta, fg_color="transparent")
        main_container.pack(fill="x", padx=20, pady=15)

        # Columna izquierda - Icono y estado
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            left_frame,
            text=icono,
            font=("Arial", 32)
        ).pack()

        ctk.CTkLabel(
            left_frame,
            text=estado_texto,
            font=("Arial", 10, "bold"),
            text_color=color_estado
        ).pack()

        # Columna central - Información
        center_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        center_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            center_frame,
            text=f"Máquina: {maquina}",
            font=("Arial", 16, "bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            center_frame,
            text=f"Fecha: {fecha}  |  Hora: {hora}  |  Duración: {duracion}h",
            font=("Arial", 13),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(5, 0))

        # Columna derecha - Fecha formateada
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.pack(side="right")

        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
            dia_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"][fecha_obj.weekday()]
            
            ctk.CTkLabel(
                right_frame,
                text=dia_semana,
                font=("Arial", 12, "bold"),
                text_color="gray"
            ).pack()
            
            ctk.CTkLabel(
                right_frame,
                text=fecha_formateada,
                font=("Arial", 11),
                text_color="gray"
            ).pack()
        except:
            pass
