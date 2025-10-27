import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, usuario_id, usuario_actual):
        super().__init__()

        self.usuario_id = usuario_id
        self.usuario_actual = usuario_actual

        self.title(f"Gimnasio - Bienvenido {usuario_actual}")
        self.geometry("700x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        titulo = ctk.CTkLabel(self, text="Tus Estadísticas", font=("Arial", 28, "bold"))
        titulo.pack(pady=20)

        frame_stats = ctk.CTkFrame(self, fg_color="transparent")
        frame_stats.pack(pady=10)

        self.crear_tarjeta(frame_stats, "Reservas Hechas", "15", "#9333EA", 0, 0)
        self.crear_tarjeta(frame_stats, "Horas Entrenadas", "42h", "#0EA5E9", 0, 1)
        self.crear_tarjeta(frame_stats, "Clases Asistidas", "10", "#22C55E", 0, 2)
        self.crear_tarjeta(frame_stats, "Progreso", "Nivel 3", "#EF4444", 0, 3)

        acciones = ctk.CTkLabel(self, text="Acciones", font=("Arial", 22, "bold"))
        acciones.pack(pady=(40, 10))

        frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        frame_acciones.pack()

        self.crear_boton_accion(frame_acciones, "Reservar Clase", "#0284C7", 0, 0)
        self.crear_boton_accion(frame_acciones, "Ver Rutinas", "#16A34A", 0, 1)
        self.crear_boton_accion(frame_acciones, "Ver Progreso", "#DC2626", 1, 0)
        self.crear_boton_accion(frame_acciones, "Historial", "#A855F7", 1, 1)

    def crear_tarjeta(self, parent, titulo, valor, color, fila, columna):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=color)
        card.grid(row=fila, column=columna, padx=15, pady=10, ipadx=25, ipady=25)

        lbl_titulo = ctk.CTkLabel(card, text=titulo, text_color="white", font=("Arial", 14, "bold"))
        lbl_titulo.pack()
        lbl_valor = ctk.CTkLabel(card, text=valor, text_color="white", font=("Arial", 26, "bold"))
        lbl_valor.pack()

    def crear_boton_accion(self, parent, texto, color, fila, columna):
        btn = ctk.CTkButton(
            parent,
            text=texto,
            fg_color=color,
            hover_color="#1E293B",
            width=180,
            height=80,
            font=("Arial", 18, "bold")
        )
        btn.grid(row=fila, column=columna, padx=20, pady=20)
