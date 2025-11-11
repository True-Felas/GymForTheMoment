import customtkinter as ctk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.Model.user_model import UserModel
from Backend.Model.rutina_model import RutinaModel
from Backend.Model.reserv_model import ReservaModel


class ProgresoView(ctk.CTkToplevel):
    def __init__(self, parent, usuario_id, usuario_nombre):
        super().__init__(parent)

        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre
        self.user_model = UserModel()
        self.rutina_model = RutinaModel()
        self.reserva_model = ReservaModel()
        
        self.title("📊 Mi Progreso")
        self.geometry("1100x750")
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
        width = 1100
        height = 750
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        """Crea la interfaz de progreso"""
        # Título
        ctk.CTkLabel(
            self,
            text="Mi Perfil y Progreso",
            font=("Arial", 36, "bold")
        ).pack(pady=20)

        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Sección de perfil
        self.crear_seccion_perfil(main_frame)

        # Separador
        ctk.CTkFrame(main_frame, height=2, fg_color="#334155").pack(fill="x", pady=20)

        # Sección de estadísticas generales
        self.crear_seccion_estadisticas(main_frame)

        # Separador
        ctk.CTkFrame(main_frame, height=2, fg_color="#334155").pack(fill="x", pady=20)

        # Sección de rutinas completadas
        self.crear_seccion_rutinas(main_frame)

        # Separador
        ctk.CTkFrame(main_frame, height=2, fg_color="#334155").pack(fill="x", pady=20)

        # Sección de progreso de nivel
        self.crear_seccion_nivel(main_frame)

        # Botón cerrar
        ctk.CTkButton(
            self,
            text="Cerrar",
            command=self.destroy,
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#64748B",
            hover_color="#475569"
        ).pack(pady=20)

    def crear_seccion_perfil(self, parent):
        """Crea la sección de perfil del usuario"""
        perfil_frame = ctk.CTkFrame(parent, corner_radius=15, fg_color="#1a1a1a")
        perfil_frame.pack(fill="x", pady=10, padx=10)

        content_frame = ctk.CTkFrame(perfil_frame, fg_color="transparent")
        content_frame.pack(pady=20, padx=30, fill="x")

        # Avatar y nombre
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=20)

        # Avatar (círculo con inicial)
        avatar_frame = ctk.CTkFrame(
            left_frame, 
            width=120, 
            height=120, 
            corner_radius=60,
            fg_color="#0284C7"
        )
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)

        ctk.CTkLabel(
            avatar_frame,
            text=self.usuario_nombre[0].upper(),
            font=("Arial", 48, "bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Botón cambiar foto
        ctk.CTkButton(
            left_frame,
            text="[IMG] Cambiar",
            command=self.cambiar_foto_perfil,
            width=120,
            height=35,
            font=("Arial", 12),
            fg_color="#334155",
            hover_color="#475569"
        ).pack(pady=10)

        # Información del usuario
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="left", fill="x", expand=True, padx=20)

        ctk.CTkLabel(
            right_frame,
            text=f"Usuario: {self.usuario_nombre}",
            font=("Arial", 28, "bold"),
            anchor="w"
        ).pack(fill="x", pady=5)

        # Obtener estadísticas
        stats = self.user_model.obtener_estadisticas(self.usuario_id)

        info_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=10)

        self.crear_badge(info_frame, "[*]", f"Nivel {stats['nivel']}", "#EAB308", 0)
        self.crear_badge(info_frame, "[OK]", f"{stats['reservas_completadas']} completadas", "#22C55E", 1)
        self.crear_badge(info_frame, "[T]", f"{stats['horas']}h entrenadas", "#0EA5E9", 2)

    def crear_badge(self, parent, icono, texto, color, columna):
        """Crea un badge de información"""
        badge = ctk.CTkFrame(parent, corner_radius=8, fg_color=color)
        badge.grid(row=0, column=columna, padx=5, sticky="w")

        content = ctk.CTkFrame(badge, fg_color="transparent")
        content.pack(padx=12, pady=8)

        ctk.CTkLabel(
            content,
            text=icono,
            font=("Arial", 16)
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            content,
            text=texto,
            font=("Arial", 13, "bold"),
            text_color="white"
        ).pack(side="left")

    def crear_seccion_estadisticas(self, parent):
        """Crea la sección de estadísticas generales"""
        ctk.CTkLabel(
            parent,
            text="Estadísticas Generales",
            font=("Arial", 24, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(10, 15), padx=10)

        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10)

        # Obtener estadísticas
        user_stats = self.user_model.obtener_estadisticas(self.usuario_id)
        rutina_stats = self.rutina_model.obtener_estadisticas_rutinas(self.usuario_id)

        # Grid de estadísticas
        stats_data = [
            ("[R]", "Reservas Totales", user_stats['reservas'], "#9333EA"),
            ("[OK]", "Reservas Completadas", user_stats['reservas_completadas'], "#22C55E"),
            ("[RT]", "Rutinas Completadas", rutina_stats['total_rutinas'], "#EAB308"),
            ("[EJ]", "Ejercicios Realizados", rutina_stats['total_ejercicios'], "#DC2626"),
        ]

        for i, (icono, titulo, valor, color) in enumerate(stats_data):
            self.crear_tarjeta_stat(stats_frame, icono, titulo, valor, color, i)

    def crear_tarjeta_stat(self, parent, icono, titulo, valor, color, indice):
        """Crea una tarjeta de estadística"""
        tarjeta = ctk.CTkFrame(parent, corner_radius=10, fg_color="#1a1a1a", border_width=2, border_color=color)
        tarjeta.grid(row=indice // 2, column=indice % 2, padx=10, pady=10, sticky="nsew")

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            tarjeta,
            text=icono,
            font=("Arial", 32)
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 12),
            text_color="gray"
        ).pack()

        ctk.CTkLabel(
            tarjeta,
            text=str(valor),
            font=("Arial", 28, "bold"),
            text_color=color
        ).pack(pady=(5, 15))

    def crear_seccion_rutinas(self, parent):
        """Crea la sección de rutinas completadas"""
        ctk.CTkLabel(
            parent,
            text="Rutinas Completadas",
            font=("Arial", 24, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(10, 15), padx=10)

        rutinas_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#1a1a1a")
        rutinas_frame.pack(fill="x", padx=10, pady=5)

        # Obtener estadísticas de rutinas
        stats = self.rutina_model.obtener_estadisticas_rutinas(self.usuario_id)

        if stats['total_rutinas'] == 0:
            ctk.CTkLabel(
                rutinas_frame,
                text="Aún no has completado ninguna rutina.\n¡Ve a la sección de Rutinas y comienza!",
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=30)
        else:
            # Mostrar rutinas por nivel
            content_frame = ctk.CTkFrame(rutinas_frame, fg_color="transparent")
            content_frame.pack(pady=20, padx=20, fill="x")

            niveles = [
                ("[+] Fácil", stats['facil'], "#22C55E"),
                ("[++] Intermedio", stats['intermedio'], "#EAB308"),
                ("[+++] Difícil", stats['dificil'], "#DC2626")
            ]

            for i, (nombre, cantidad, color) in enumerate(niveles):
                nivel_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                nivel_frame.grid(row=0, column=i, padx=15, sticky="nsew")
                content_frame.grid_columnconfigure(i, weight=1)

                ctk.CTkLabel(
                    nivel_frame,
                    text=nombre,
                    font=("Arial", 14, "bold")
                ).pack()

                ctk.CTkLabel(
                    nivel_frame,
                    text=str(cantidad),
                    font=("Arial", 32, "bold"),
                    text_color=color
                ).pack(pady=5)

                ctk.CTkLabel(
                    nivel_frame,
                    text="completadas",
                    font=("Arial", 11),
                    text_color="gray"
                ).pack()

    def crear_seccion_nivel(self, parent):
        """Crea la sección de progreso de nivel"""
        ctk.CTkLabel(
            parent,
            text="Progreso de Nivel",
            font=("Arial", 24, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(10, 15), padx=10)

        nivel_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#1a1a1a")
        nivel_frame.pack(fill="x", padx=10, pady=5)

        content_frame = ctk.CTkFrame(nivel_frame, fg_color="transparent")
        content_frame.pack(pady=20, padx=30, fill="x")

        # Obtener estadísticas
        stats = self.user_model.obtener_estadisticas(self.usuario_id)
        nivel_actual = stats['nivel']
        reservas_completadas = stats['reservas_para_nivel']
        progreso_nivel = reservas_completadas % 3
        faltan = 3 - progreso_nivel

        # Nivel actual
        ctk.CTkLabel(
            content_frame,
            text=f"Nivel Actual: {nivel_actual}",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        # Barra de progreso
        progress_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        progress_frame.pack(fill="x", pady=15)

        ctk.CTkLabel(
            progress_frame,
            text=f"Progreso hacia Nivel {nivel_actual + 1}:",
            font=("Arial", 14)
        ).pack(pady=5)

        # Crear barra visual
        barra_container = ctk.CTkFrame(progress_frame, height=30, corner_radius=15, fg_color="#334155")
        barra_container.pack(fill="x", padx=50, pady=10)

        porcentaje = (progreso_nivel / 3) * 100
        barra_progreso = ctk.CTkFrame(
            barra_container, 
            height=30, 
            corner_radius=15,
            fg_color="#22C55E"
        )
        barra_progreso.place(x=0, y=0, relwidth=porcentaje/100, relheight=1)

        ctk.CTkLabel(
            barra_container,
            text=f"{progreso_nivel}/3 reservas",
            font=("Arial", 12, "bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Mensaje motivacional
        if faltan == 0:
            mensaje = "¡Completa una reserva más para subir de nivel!"
        else:
            mensaje = f"Te faltan {faltan} reservas completadas para el siguiente nivel"

        ctk.CTkLabel(
            progress_frame,
            text=mensaje,
            font=("Arial", 13),
            text_color="#22C55E" if faltan <= 1 else "gray"
        ).pack(pady=5)

    def cambiar_foto_perfil(self):
        """Muestra mensaje informativo sobre cambio de foto"""
        msg = ctk.CTkToplevel(self)
        msg.title("Cambiar Foto")
        msg.geometry("400x200")
        msg.transient(self)
        msg.grab_set()

        # Centrar
        msg.update_idletasks()
        x = (msg.winfo_screenwidth() // 2) - 200
        y = (msg.winfo_screenheight() // 2) - 100
        msg.geometry(f'400x200+{x}+{y}')

        ctk.CTkLabel(
            msg,
            text="[IMG]",
            font=("Arial", 48)
        ).pack(pady=20)

        ctk.CTkLabel(
            msg,
            text="Función en desarrollo",
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        ctk.CTkLabel(
            msg,
            text="Pronto podrás cambiar tu foto de perfil",
            font=("Arial", 12),
            text_color="gray"
        ).pack(pady=5)

        ctk.CTkButton(
            msg,
            text="Entendido",
            command=msg.destroy,
            width=150,
            height=40,
            font=("Arial", 14, "bold")
        ).pack(pady=15)
