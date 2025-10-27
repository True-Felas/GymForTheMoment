import customtkinter as ctk
from datetime import datetime, date
from tkcalendar import Calendar


class ReservasView(ctk.CTkToplevel):
    def __init__(self, parent, usuario_id, callback_actualizar=None):
        super().__init__(parent)

        self.usuario_id = usuario_id
        self.callback_actualizar = callback_actualizar
        self.fecha_seleccionada = None
        self.clase_seleccionada = None
        self.hora_seleccionada = None

        self.title("Reservar Clase")
        self.geometry("900x700")
        self.resizable(False, False)

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
        """Crea la interfaz de reservas con calendario"""
        from Backend.Model.reserv_model import ReservaModel
        self.reserva_model = ReservaModel()

        # Título
        ctk.CTkLabel(
            self,
            text="📅 Nueva Reserva",
            font=("Arial", 32, "bold")
        ).pack(pady=20)

        # Frame principal con dos columnas
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # === COLUMNA IZQUIERDA: Calendario y Clases ===
        left_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Paso 1: Seleccionar Fecha
        ctk.CTkLabel(
            left_frame,
            text="1️⃣ Selecciona una fecha:",
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 10))

        # Calendario
        self.calendario = Calendar(
            left_frame,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            mindate=date.today(),
            font=("Arial", 11),
            background='#1f538d',
            foreground='white',
            selectbackground='#0284C7',
            selectforeground='white',
            headersbackground='#0284C7',
            headersforeground='white',
            normalbackground='#2b2b2b',
            normalforeground='white',
            weekendbackground='#404040',
            weekendforeground='white',
            othermonthbackground='#1a1a1a',
            othermonthforeground='gray'
        )
        self.calendario.pack(pady=10, padx=20)
        self.calendario.bind("<<CalendarSelected>>", self.on_fecha_seleccionada)

        # Paso 2: Seleccionar Clase
        ctk.CTkLabel(
            left_frame,
            text="2️⃣ Selecciona una clase:",
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 10))

        # Frame scrollable para clases
        clases_frame = ctk.CTkScrollableFrame(left_frame, height=150)
        clases_frame.pack(pady=10, padx=20, fill="x")

        self.botones_clases = {}
        for clase in ReservaModel.CLASES_DISPONIBLES:
            btn = ctk.CTkButton(
                clases_frame,
                text=clase,
                command=lambda c=clase: self.on_clase_seleccionada(c),
                fg_color="transparent",
                border_width=2,
                border_color="#0284C7",
                hover_color="#0284C7",
                height=40,
                font=("Arial", 14)
            )
            btn.pack(pady=5, padx=5, fill="x")
            self.botones_clases[clase] = btn

        # === COLUMNA DERECHA: Horarios y Confirmación ===
        right_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Paso 3: Seleccionar Hora
        ctk.CTkLabel(
            right_frame,
            text="3️⃣ Selecciona un horario:",
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 10))

        # Leyenda de colores
        leyenda_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        leyenda_frame.pack(pady=5)

        ctk.CTkLabel(
            leyenda_frame,
            text="🟢 Disponible",
            font=("Arial", 10),
            text_color="#22C55E"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            leyenda_frame,
            text="🟡 Pocas plazas",
            font=("Arial", 10),
            text_color="#EAB308"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            leyenda_frame,
            text="🔴 Completo",
            font=("Arial", 10),
            text_color="#DC2626"
        ).pack(side="left", padx=10)

        # Frame scrollable para horarios
        self.horarios_frame = ctk.CTkScrollableFrame(right_frame, height=250)
        self.horarios_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Mensaje inicial
        ctk.CTkLabel(
            self.horarios_frame,
            text="Selecciona una fecha y clase\npara ver horarios disponibles",
            font=("Arial", 13),
            text_color="gray"
        ).pack(pady=50)

        # Resumen de la reserva
        self.resumen_frame = ctk.CTkFrame(right_frame, corner_radius=10, fg_color="#1a1a1a")
        self.resumen_frame.pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(
            self.resumen_frame,
            text="📋 Resumen de tu reserva:",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.resumen_label = ctk.CTkLabel(
            self.resumen_frame,
            text="Aún no has seleccionado nada",
            font=("Arial", 12),
            text_color="gray"
        )
        self.resumen_label.pack(pady=10)

        # Label de error
        self.error_label = ctk.CTkLabel(
            right_frame,
            text="",
            text_color="red",
            font=("Arial", 12)
        )
        self.error_label.pack(pady=5)

        # Frame de botones
        buttons_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        buttons_frame.pack(pady=10)

        # Botón Confirmar
        self.boton_confirmar = ctk.CTkButton(
            buttons_frame,
            text="✅ Confirmar Reserva",
            command=self.guardar_reserva,
            fg_color="#22C55E",
            hover_color="#16A34A",
            width=180,
            height=50,
            font=("Arial", 15, "bold"),
            state="disabled"
        )
        self.boton_confirmar.pack(side="left", padx=5)

        # Botón Cancelar
        ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=self.destroy,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            width=180,
            height=50,
            font=("Arial", 15, "bold")
        ).pack(side="left", padx=5)

    def on_fecha_seleccionada(self, event):
        """Se ejecuta cuando se selecciona una fecha del calendario"""
        self.fecha_seleccionada = self.calendario.get_date()
        self.actualizar_horarios()
        self.actualizar_resumen()

    def on_clase_seleccionada(self, clase):
        """Se ejecuta cuando se selecciona una clase"""
        self.clase_seleccionada = clase

        # Actualizar colores de botones
        for nombre, boton in self.botones_clases.items():
            if nombre == clase:
                boton.configure(fg_color="#0284C7", border_color="#0284C7")
            else:
                boton.configure(fg_color="transparent", border_color="#0284C7")

        self.actualizar_horarios()
        self.actualizar_resumen()

    def actualizar_horarios(self):
        """Actualiza la lista de horarios con indicadores de capacidad"""
        # Limpiar frame de horarios
        for widget in self.horarios_frame.winfo_children():
            widget.destroy()

        if not self.fecha_seleccionada or not self.clase_seleccionada:
            ctk.CTkLabel(
                self.horarios_frame,
                text="Selecciona una fecha y clase\npara ver horarios disponibles",
                font=("Arial", 13),
                text_color="gray"
            ).pack(pady=50)
            return

        # Obtener información de todos los horarios
        info_horarios = self.reserva_model.obtener_info_horarios(
            self.fecha_seleccionada,
            self.clase_seleccionada
        )

        # Mostrar horarios con indicadores de capacidad
        self.botones_horarios = {}
        for info in info_horarios:
            hora = info['hora']
            reservas = info['reservas']
            capacidad = info['capacidad_maxima']
            cupos = info['cupos_disponibles']
            disponible = info['disponible']
            porcentaje = info['porcentaje_ocupacion']

            # Determinar color según ocupación
            if not disponible:
                # Completo (rojo)
                color_fg = "#DC2626"
                color_border = "#DC2626"
                color_hover = "#B91C1C"
                icono = "🔴"
                estado = "COMPLETO"
                enabled = False
            elif porcentaje >= 70:
                # Pocas plazas (amarillo)
                color_fg = "transparent"
                color_border = "#EAB308"
                color_hover = "#EAB308"
                icono = "🟡"
                estado = f"{cupos} plazas"
                enabled = True
            else:
                # Disponible (verde)
                color_fg = "transparent"
                color_border = "#22C55E"
                color_hover = "#22C55E"
                icono = "🟢"
                estado = f"{cupos} plazas"
                enabled = True

            # Crear frame para el botón y la info
            horario_container = ctk.CTkFrame(self.horarios_frame, fg_color="transparent")
            horario_container.pack(pady=5, padx=10, fill="x")

            btn = ctk.CTkButton(
                horario_container,
                text=f"{icono} {hora}  -  {estado}",
                command=lambda h=hora: self.on_hora_seleccionada(h) if disponible else None,
                fg_color=color_fg if enabled else "#DC2626",
                border_width=2,
                border_color=color_border,
                hover_color=color_hover if enabled else "#DC2626",
                height=45,
                font=("Arial", 14, "bold"),
                state="normal" if enabled else "disabled"
            )
            btn.pack(fill="x")

            if enabled:
                self.botones_horarios[hora] = btn

    def on_hora_seleccionada(self, hora):
        """Se ejecuta cuando se selecciona un horario"""
        self.hora_seleccionada = hora
        self.error_label.configure(text="")

        # Actualizar colores de botones
        for h, boton in self.botones_horarios.items():
            if h == hora:
                boton.configure(fg_color="#22C55E", border_color="#22C55E")
            else:
                # Restaurar color según disponibilidad
                info = self.reserva_model.obtener_info_horarios(
                    self.fecha_seleccionada,
                    self.clase_seleccionada
                )
                for i in info:
                    if i['hora'] == h:
                        if i['porcentaje_ocupacion'] >= 70:
                            boton.configure(fg_color="transparent", border_color="#EAB308")
                        else:
                            boton.configure(fg_color="transparent", border_color="#22C55E")

        self.actualizar_resumen()
        self.boton_confirmar.configure(state="normal")

    def actualizar_resumen(self):
        """Actualiza el resumen de la reserva"""
        if not self.fecha_seleccionada and not self.clase_seleccionada and not self.hora_seleccionada:
            texto = "Aún no has seleccionado nada"
        else:
            fecha_texto = f"📅 Fecha: {self.fecha_seleccionada}" if self.fecha_seleccionada else ""
            clase_texto = f"\n🏋️ Clase: {self.clase_seleccionada}" if self.clase_seleccionada else ""
            hora_texto = f"\n🕐 Hora: {self.hora_seleccionada}" if self.hora_seleccionada else ""
            texto = fecha_texto + clase_texto + hora_texto

        self.resumen_label.configure(text=texto, text_color="white" if self.hora_seleccionada else "gray")

    def guardar_reserva(self):
        """Guarda la reserva en la base de datos"""
        if not self.fecha_seleccionada or not self.clase_seleccionada or not self.hora_seleccionada:
            self.error_label.configure(text="Por favor, completa todos los campos")
            return

        # Verificar nuevamente que hay cupo (por si alguien reservó mientras tanto)
        if not self.reserva_model.hay_cupo_disponible(
                self.fecha_seleccionada,
                self.clase_seleccionada,
                self.hora_seleccionada
        ):
            self.error_label.configure(text="Lo sentimos, esta clase se llenó")
            self.actualizar_horarios()  # Actualizar la lista
            return

        # Crear la reserva
        if self.reserva_model.crear_reserva(
                self.usuario_id,
                self.clase_seleccionada,
                self.fecha_seleccionada,
                self.hora_seleccionada
        ):
            # Llamar al callback para actualizar estadísticas
            if self.callback_actualizar:
                self.callback_actualizar()

            self.destroy()
            self.mostrar_mensaje_exito()
        else:
            self.error_label.configure(text="Error al crear la reserva o clase llena")

    def mostrar_mensaje_exito(self):
        """Muestra un mensaje de éxito"""
        msg = ctk.CTkToplevel(self.master)
        msg.title("✅ Éxito")
        msg.geometry("450x250")
        msg.resizable(False, False)

        # Centrar mensaje
        msg.update_idletasks()
        x = (msg.winfo_screenwidth() // 2) - (450 // 2)
        y = (msg.winfo_screenheight() // 2) - (250 // 2)
        msg.geometry(f'450x250+{x}+{y}')

        # Hacer modal
        msg.transient(self.master)
        msg.grab_set()

        ctk.CTkLabel(
            msg,
            text="✅",
            font=("Arial", 48)
        ).pack(pady=20)

        ctk.CTkLabel(
            msg,
            text="¡Reserva creada con éxito!",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            msg,
            text=f"{self.clase_seleccionada} - {self.fecha_seleccionada} a las {self.hora_seleccionada}",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=10)

        ctk.CTkButton(
            msg,
            text="Aceptar",
            command=msg.destroy,
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#22C55E",
            hover_color="#16A34A"
        ).pack(pady=20)