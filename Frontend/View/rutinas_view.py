import customtkinter as ctk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.Model.rutina_model import RutinaModel


class RutinasView(ctk.CTkToplevel):
    def __init__(self, parent, usuario_id):
        super().__init__(parent)

        self.usuario_id = usuario_id
        self.rutina_model = RutinaModel()
        self.nivel_seleccionado = None
        self.ejercicios_completados = []
        
        self.title("💪 Rutinas de Entrenamiento")
        self.geometry("1000x750")
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
        width = 1000
        height = 750
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def crear_interfaz(self):
        """Crea la interfaz de rutinas"""
        # Título
        ctk.CTkLabel(
            self,
            text="Rutinas de Entrenamiento",
            font=("Arial", 36, "bold")
        ).pack(pady=20)

        # Subtítulo
        ctk.CTkLabel(
            self,
            text="Elige tu nivel y comienza a entrenar",
            font=("Arial", 16),
            text_color="gray"
        ).pack(pady=(0, 20))

        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Obtener todas las rutinas
        rutinas = self.rutina_model.obtener_todas_rutinas()

        # Crear tarjetas de rutinas
        cards_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.pack(fill="both", expand=True)

        # Configurar grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)

        # Crear tarjeta para cada nivel
        self.crear_tarjeta_rutina(cards_frame, "facil", rutinas["facil"], "#22C55E", 0)
        self.crear_tarjeta_rutina(cards_frame, "intermedio", rutinas["intermedio"], "#EAB308", 1)
        self.crear_tarjeta_rutina(cards_frame, "dificil", rutinas["dificil"], "#DC2626", 2)

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

    def crear_tarjeta_rutina(self, parent, nivel, rutina, color, columna):
        """Crea una tarjeta para mostrar una rutina"""
        tarjeta = ctk.CTkFrame(
            parent,
            corner_radius=15,
            border_width=3,
            border_color=color,
            fg_color="#1a1a1a"
        )
        tarjeta.grid(row=0, column=columna, padx=15, pady=10, sticky="nsew")

        # Icono según nivel
        iconos = {
            "facil": "[+]",
            "intermedio": "[++]",
            "dificil": "[+++]"
        }

        # Encabezado
        ctk.CTkLabel(
            tarjeta,
            text=iconos[nivel],
            font=("Arial", 48)
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            tarjeta,
            text=rutina["nombre"],
            font=("Arial", 20, "bold"),
            text_color=color
        ).pack(pady=5)

        ctk.CTkLabel(
            tarjeta,
            text=rutina["descripcion"],
            font=("Arial", 12),
            text_color="gray",
            wraplength=200
        ).pack(pady=5)

        # Duración
        duracion_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        duracion_frame.pack(pady=10)

        ctk.CTkLabel(
            duracion_frame,
            text="Duración:",
            font=("Arial", 13, "bold")
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            duracion_frame,
            text=rutina["duracion"],
            font=("Arial", 13)
        ).pack(side="left")

        # Número de ejercicios
        ctk.CTkLabel(
            tarjeta,
            text=f"{len(rutina['ejercicios'])} ejercicios",
            font=("Arial", 12),
            text_color="gray"
        ).pack(pady=5)

        # Botón para ver detalles
        ctk.CTkButton(
            tarjeta,
            text="Ver Rutina",
            command=lambda: self.mostrar_detalle_rutina(nivel, rutina),
            fg_color=color,
            hover_color=self.oscurecer_color(color),
            width=180,
            height=40,
            font=("Arial", 14, "bold")
        ).pack(pady=20)

    def oscurecer_color(self, color):
        """Oscurece un color hex para el hover"""
        colores_oscuros = {
            "#22C55E": "#16A34A",
            "#EAB308": "#CA8A04",
            "#DC2626": "#B91C1C"
        }
        return colores_oscuros.get(color, color)

    def mostrar_detalle_rutina(self, nivel, rutina):
        """Muestra el detalle completo de una rutina"""
        # Crear ventana de detalle
        detalle = ctk.CTkToplevel(self)
        detalle.title(f"{rutina['nombre']}")
        detalle.geometry("800x700")
        detalle.transient(self)
        detalle.grab_set()

        # Centrar
        detalle.update_idletasks()
        x = (detalle.winfo_screenwidth() // 2) - 400
        y = (detalle.winfo_screenheight() // 2) - 350
        detalle.geometry(f'800x700+{x}+{y}')

        # Título
        ctk.CTkLabel(
            detalle,
            text=rutina["nombre"],
            font=("Arial", 32, "bold")
        ).pack(pady=20)

        # Descripción y duración
        info_frame = ctk.CTkFrame(detalle, fg_color="transparent")
        info_frame.pack(pady=10)

        ctk.CTkLabel(
            info_frame,
            text=f"Duración: {rutina['duracion']} | {len(rutina['ejercicios'])} ejercicios",
            font=("Arial", 14),
            text_color="gray"
        ).pack()

        # Lista de ejercicios
        ctk.CTkLabel(
            detalle,
            text="Ejercicios:",
            font=("Arial", 20, "bold")
        ).pack(pady=(20, 10))

        # Frame scrollable para ejercicios
        ejercicios_frame = ctk.CTkScrollableFrame(detalle, fg_color="transparent")
        ejercicios_frame.pack(pady=10, padx=30, fill="both", expand=True)

        self.ejercicios_completados = []

        for i, ejercicio in enumerate(rutina["ejercicios"], 1):
            self.crear_item_ejercicio(
                ejercicios_frame, 
                i, 
                ejercicio["nombre"],
                ejercicio["series"],
                ejercicio["repeticiones"],
                ejercicio["descanso"]
            )

        # Frame de botones
        botones_frame = ctk.CTkFrame(detalle, fg_color="transparent")
        botones_frame.pack(pady=20)

        # Botón para marcar como completada
        ctk.CTkButton(
            botones_frame,
            text="Marcar Rutina Completada",
            command=lambda: self.completar_rutina(nivel, len(rutina["ejercicios"]), detalle),
            fg_color="#22C55E",
            hover_color="#16A34A",
            width=250,
            height=50,
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=10)

        # Botón cerrar
        ctk.CTkButton(
            botones_frame,
            text="Cerrar",
            command=detalle.destroy,
            fg_color="#64748B",
            hover_color="#475569",
            width=150,
            height=50,
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=10)

    def crear_item_ejercicio(self, parent, numero, nombre, series, repeticiones, descanso):
        """Crea un item para mostrar un ejercicio"""
        item_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#1a1a1a")
        item_frame.pack(pady=5, padx=10, fill="x")

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)

        # Número
        ctk.CTkLabel(
            content_frame,
            text=f"{numero}.",
            font=("Arial", 16, "bold"),
            width=30
        ).pack(side="left", padx=(0, 10))

        # Nombre del ejercicio
        ctk.CTkLabel(
            content_frame,
            text=nombre,
            font=("Arial", 15, "bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        # Detalles
        detalles_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        detalles_frame.pack(side="right")

        ctk.CTkLabel(
            detalles_frame,
            text=f"{series}x{repeticiones}",
            font=("Arial", 13),
            text_color="#22C55E"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            detalles_frame,
            text=f"Descanso: {descanso}",
            font=("Arial", 12),
            text_color="gray"
        ).pack(side="left")

    def completar_rutina(self, nivel, num_ejercicios, ventana):
        """Marca la rutina como completada"""
        resultado = self.rutina_model.marcar_rutina_completada(
            self.usuario_id, 
            nivel, 
            num_ejercicios
        )

        if resultado:
            self.mostrar_mensaje_exito(ventana)
        else:
            self.mostrar_mensaje_error(ventana)

    def mostrar_mensaje_exito(self, parent):
        """Muestra mensaje de éxito"""
        msg = ctk.CTkToplevel(parent)
        msg.title("¡Éxito!")
        msg.geometry("400x250")
        msg.transient(parent)
        msg.grab_set()

        # Centrar
        msg.update_idletasks()
        x = (msg.winfo_screenwidth() // 2) - 200
        y = (msg.winfo_screenheight() // 2) - 125
        msg.geometry(f'400x250+{x}+{y}')

        ctk.CTkLabel(
            msg,
            text="[OK]",
            font=("Arial", 64)
        ).pack(pady=20)

        ctk.CTkLabel(
            msg,
            text="¡Rutina Completada!",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            msg,
            text="¡Sigue así, vas muy bien!",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=5)

        ctk.CTkButton(
            msg,
            text="Aceptar",
            command=lambda: [msg.destroy(), parent.destroy()],
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#22C55E",
            hover_color="#16A34A"
        ).pack(pady=20)

    def mostrar_mensaje_error(self, parent):
        """Muestra mensaje de error"""
        msg = ctk.CTkToplevel(parent)
        msg.title("Error")
        msg.geometry("400x200")
        msg.transient(parent)
        msg.grab_set()

        # Centrar
        msg.update_idletasks()
        x = (msg.winfo_screenwidth() // 2) - 200
        y = (msg.winfo_screenheight() // 2) - 100
        msg.geometry(f'400x200+{x}+{y}')

        ctk.CTkLabel(
            msg,
            text="[X]",
            font=("Arial", 48)
        ).pack(pady=20)

        ctk.CTkLabel(
            msg,
            text="Error al guardar la rutina",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        ctk.CTkButton(
            msg,
            text="Cerrar",
            command=msg.destroy,
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C"
        ).pack(pady=20)
