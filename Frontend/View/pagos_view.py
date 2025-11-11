import customtkinter as ctk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.Model.pago_model import PagoModel
from Backend.Model.user_model import UserModel
from datetime import datetime


class PagosView(ctk.CTkToplevel):
    def __init__(self, parent, usuario_id, es_admin=False):
        super().__init__(parent)

        self.usuario_id = usuario_id
        self.es_admin = es_admin
        self.pago_model = PagoModel()
        self.user_model = UserModel()
        
        titulo = "Gestión de Pagos" if es_admin else "Mis Pagos"
        self.title(titulo)
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
        """Crea la interfaz de pagos"""
        # Generar recibos de ejemplo automáticamente
        self.pago_model.generar_recibos_ejemplo()
        
        # Título
        titulo_texto = "Gestión de Pagos" if self.es_admin else "Mis Pagos Mensuales"
        ctk.CTkLabel(
            self,
            text=titulo_texto,
            font=("Arial", 36, "bold")
        ).pack(pady=20)

        if self.es_admin:
            self.crear_interfaz_admin()
        else:
            self.crear_interfaz_usuario()

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

    def crear_interfaz_admin(self):
        """Interfaz para administradores"""
        # Pestañas
        tabview = ctk.CTkTabview(self, width=900, height=550)
        tabview.pack(pady=10, padx=30)

        tab_usuarios = tabview.add("Gestión Usuarios")
        tab_estadisticas = tabview.add("Estadísticas")
        tab_morosos = tabview.add("Usuarios Morosos")
        tab_generar = tabview.add("Generar Recibos")

        # === TAB 0: Gestión de Usuarios (NUEVO) ===
        self.crear_tab_gestion_usuarios(tab_usuarios)

        # === TAB 1: Estadísticas ===
        self.crear_tab_estadisticas(tab_estadisticas)

        # === TAB 2: Morosos ===
        self.crear_tab_morosos(tab_morosos)

        # === TAB 3: Generar Recibos ===
        self.crear_tab_generar_recibos(tab_generar)

    def crear_tab_gestion_usuarios(self, parent):
        """Crea la pestaña de gestión de usuarios"""
        ctk.CTkLabel(
            parent,
            text="Gestión de Usuarios y Pagos",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            parent,
            text="Control completo de usuarios y sus pagos para pruebas",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=(0, 15))

        # Frame scrollable para usuarios
        usuarios_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        usuarios_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Obtener todos los usuarios
        try:
            from Backend.Model.user_model import UserModel
            user_model = UserModel()
            
            # Consulta manual para obtener todos los usuarios
            from Backend.DataBase.database import Database
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, nivel, reservas_completadas FROM usuarios ORDER BY id")
            usuarios = cursor.fetchall()
            cursor.close()
            conn.close()

            if not usuarios:
                ctk.CTkLabel(
                    usuarios_frame,
                    text="No hay usuarios registrados",
                    font=("Arial", 16),
                    text_color="gray"
                ).pack(pady=50)
            else:
                for usuario_id, nombre, nivel, reservas_comp in usuarios:
                    self.crear_tarjeta_usuario_admin(usuarios_frame, usuario_id, nombre, nivel, reservas_comp)

        except Exception as e:
            ctk.CTkLabel(
                usuarios_frame,
                text=f"Error al cargar usuarios: {str(e)}",
                font=("Arial", 14),
                text_color="red"
            ).pack(pady=20)

    def crear_tarjeta_usuario_admin(self, parent, usuario_id, nombre, nivel, reservas_comp):
        """Crea una tarjeta para gestionar un usuario"""
        tarjeta = ctk.CTkFrame(parent, corner_radius=10, border_width=2, border_color="#0EA5E9", fg_color="#1a1a1a")
        tarjeta.pack(pady=8, padx=10, fill="x")

        main_container = ctk.CTkFrame(tarjeta, fg_color="transparent")
        main_container.pack(fill="x", padx=20, pady=15)

        # Información del usuario
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            left_frame,
            text=f"👤 {nombre}",
            font=("Arial", 18, "bold"),
            anchor="w"
        ).pack(fill="x")

        # Obtener estadísticas de pagos
        pagos = self.pago_model.obtener_pagos_usuario(usuario_id)
        pagos_pendientes = sum(1 for p in pagos if p[4] == 0)  # pagado == 0
        pagos_realizados = sum(1 for p in pagos if p[4] == 1)  # pagado == 1
        deuda_total = sum(p[3] for p in pagos if p[4] == 0)  # monto si no pagado

        info_text = f"ID: {usuario_id} | Nivel: {nivel} | Reservas: {reservas_comp} | Pagos: {pagos_realizados} realizados, {pagos_pendientes} pendientes | Deuda: {deuda_total:.2f}€"
        
        ctk.CTkLabel(
            left_frame,
            text=info_text,
            font=("Arial", 12),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(5, 0))

        # Botones de acción (disposición vertical para mejor legibilidad)
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.pack(side="right", padx=(20, 0))

        ctk.CTkButton(
            right_frame,
            text="📋 Ver Pagos",
            command=lambda: self.ver_pagos_usuario_admin(usuario_id, nombre),
            width=150,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#0EA5E9",
            hover_color="#0284C7"
        ).pack(pady=3)

        ctk.CTkButton(
            right_frame,
            text="❌ Marcar Impagos",
            command=lambda: self.marcar_todos_impagos(usuario_id, nombre),
            width=150,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C"
        ).pack(pady=3)

        ctk.CTkButton(
            right_frame,
            text="✓ Marcar Pagados",
            command=lambda: self.marcar_todos_pagados(usuario_id, nombre),
            width=150,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#22C55E",
            hover_color="#16A34A"
        ).pack(pady=3)

    def ver_pagos_usuario_admin(self, usuario_id, nombre):
        """Muestra todos los pagos de un usuario con opciones de gestión"""
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Pagos de {nombre}")
        ventana.geometry("800x600")
        ventana.transient(self)
        ventana.grab_set()

        # Centrar
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - 400
        y = (ventana.winfo_screenheight() // 2) - 300
        ventana.geometry(f'800x600+{x}+{y}')

        ctk.CTkLabel(
            ventana,
            text=f"Gestión de Pagos - {nombre}",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Frame scrollable
        pagos_frame = ctk.CTkScrollableFrame(ventana, fg_color="transparent")
        pagos_frame.pack(pady=10, padx=30, fill="both", expand=True)

        pagos = self.pago_model.obtener_pagos_usuario(usuario_id)

        if not pagos:
            ctk.CTkLabel(
                pagos_frame,
                text="No hay pagos registrados para este usuario",
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=50)
        else:
            for pago in pagos:
                self.crear_tarjeta_pago_admin(pagos_frame, pago, ventana)

        # Botones de acción masiva
        botones_frame = ctk.CTkFrame(ventana, fg_color="transparent")
        botones_frame.pack(pady=15)

        ctk.CTkButton(
            botones_frame,
            text="❌ Marcar Todos como Impagos",
            command=lambda: [self.marcar_todos_impagos(usuario_id, nombre), ventana.destroy()],
            width=250,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botones_frame,
            text="🚪 Cerrar",
            command=ventana.destroy,
            width=150,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#64748B",
            hover_color="#475569"
        ).pack(side="left", padx=10)

    def crear_tarjeta_pago_admin(self, parent, pago, ventana_padre):
        """Crea una tarjeta de pago con opciones de administración"""
        pago_id, mes, anio, monto, pagado, fecha_pago = pago

        # Determinar color según estado
        if pagado:
            color_border = "#22C55E"
            icono = "[OK]"
            estado_texto = "PAGADO"
            color_estado = "#22C55E"
        else:
            color_border = "#DC2626"
            icono = "[!]"
            estado_texto = "PENDIENTE"
            color_estado = "#DC2626"

        # Nombre del mes
        nombre_mes = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes]

        tarjeta = ctk.CTkFrame(parent, corner_radius=10, border_width=2, border_color=color_border, fg_color="#1a1a1a")
        tarjeta.pack(pady=8, padx=10, fill="x")

        main_container = ctk.CTkFrame(tarjeta, fg_color="transparent")
        main_container.pack(fill="x", padx=20, pady=15)

        # Icono y estado
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            left_frame,
            text=icono,
            font=("Arial", 28)
        ).pack()

        ctk.CTkLabel(
            left_frame,
            text=estado_texto,
            font=("Arial", 10, "bold"),
            text_color=color_estado
        ).pack()

        # Información del pago
        center_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        center_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            center_frame,
            text=f"{nombre_mes} {anio}",
            font=("Arial", 16, "bold"),
            anchor="w"
        ).pack(fill="x")

        info_text = f"Monto: {monto:.2f}€"
        if pagado and fecha_pago:
            info_text += f"  |  Fecha de pago: {fecha_pago}"

        ctk.CTkLabel(
            center_frame,
            text=info_text,
            font=("Arial", 12),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(5, 0))

        # Botones de acción
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.pack(side="right")

        if pagado:
            # Si está pagado, botón para marcar como impago
            ctk.CTkButton(
                right_frame,
                text="❌ Marcar Impago",
                command=lambda: [self.cambiar_estado_pago(pago_id, 0), ventana_padre.destroy(), self.ver_pagos_usuario_admin(*ventana_padre.title().split("Pagos de ")[1:])],
                width=150,
                height=40,
                font=("Arial", 13, "bold"),
                fg_color="#DC2626",
                hover_color="#B91C1C"
            ).pack()
        else:
            # Si está pendiente, botón para marcar como pagado
            ctk.CTkButton(
                right_frame,
                text="✓ Marcar Pagado",
                command=lambda: [self.cambiar_estado_pago(pago_id, 1), ventana_padre.destroy(), self.ver_pagos_usuario_admin(*ventana_padre.title().split("Pagos de ")[1:])],
                width=150,
                height=40,
                font=("Arial", 13, "bold"),
                fg_color="#22C55E",
                hover_color="#16A34A"
            ).pack()

    def cambiar_estado_pago(self, pago_id, nuevo_estado):
        """Cambia el estado de pago de un recibo"""
        try:
            from Backend.DataBase.database import Database
            from datetime import datetime
            
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            if nuevo_estado == 1:
                # Marcar como pagado
                fecha_actual = datetime.now().strftime('%Y-%m-%d')
                cursor.execute(
                    "UPDATE pagos SET pagado = 1, fecha_pago = ? WHERE id = ?",
                    (fecha_actual, pago_id)
                )
            else:
                # Marcar como impago
                cursor.execute(
                    "UPDATE pagos SET pagado = 0, fecha_pago = NULL WHERE id = ?",
                    (pago_id,)
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al cambiar estado: {e}")
            return False

    def marcar_todos_impagos(self, usuario_id, nombre):
        """Marca todos los pagos de un usuario como impagos"""
        try:
            from Backend.DataBase.database import Database
            
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE pagos SET pagado = 0, fecha_pago = NULL WHERE usuario_id = ?",
                (usuario_id,)
            )
            
            filas_afectadas = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            # Mostrar confirmación
            self.mostrar_mensaje_admin(
                f"✓ Todos los pagos de {nombre} marcados como IMPAGOS",
                f"{filas_afectadas} recibos actualizados",
                "#EAB308"
            )
            
            # Actualizar vista
            self.after(1500, lambda: [self.destroy(), PagosView(self.master, self.usuario_id, True)])
            
        except Exception as e:
            print(f"Error al marcar impagos: {e}")

    def marcar_todos_pagados(self, usuario_id, nombre):
        """Marca todos los pagos de un usuario como pagados"""
        try:
            from Backend.DataBase.database import Database
            from datetime import datetime
            
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                "UPDATE pagos SET pagado = 1, fecha_pago = ? WHERE usuario_id = ?",
                (fecha_actual, usuario_id)
            )
            
            filas_afectadas = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            # Mostrar confirmación
            self.mostrar_mensaje_admin(
                f"✓ Todos los pagos de {nombre} marcados como PAGADOS",
                f"{filas_afectadas} recibos actualizados",
                "#22C55E"
            )
            
            # Actualizar vista
            self.after(1500, lambda: [self.destroy(), PagosView(self.master, self.usuario_id, True)])
            
        except Exception as e:
            print(f"Error al marcar pagados: {e}")

    def mostrar_mensaje_admin(self, titulo, mensaje, color):
        """Muestra un mensaje temporal de confirmación"""
        msg = ctk.CTkToplevel(self)
        msg.title("Confirmación")
        msg.geometry("450x200")
        msg.transient(self)
        msg.grab_set()

        # Centrar
        msg.update_idletasks()
        x = (msg.winfo_screenwidth() // 2) - 225
        y = (msg.winfo_screenheight() // 2) - 100
        msg.geometry(f'450x200+{x}+{y}')

        ctk.CTkLabel(
            msg,
            text="[OK]",
            font=("Arial", 40),
            text_color=color
        ).pack(pady=20)

        ctk.CTkLabel(
            msg,
            text=titulo,
            font=("Arial", 18, "bold")
        ).pack(pady=5)

        ctk.CTkLabel(
            msg,
            text=mensaje,
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=5)

        # Cerrar automáticamente después de 1.5 segundos
        msg.after(1500, msg.destroy)

    def crear_tab_estadisticas(self, parent):
        """Crea la pestaña de estadísticas"""
        stats = self.pago_model.obtener_estadisticas_pagos()

        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            stats_frame,
            text="Resumen General de Pagos",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Grid de estadísticas
        grid_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        grid_frame.pack(pady=20, padx=50, fill="both", expand=True)

        stats_data = [
            ("[R]", "Recibos Generados", stats['total_recibos'], "#9333EA"),
            ("[OK]", "Pagos Realizados", stats['pagos_realizados'], "#22C55E"),
            ("[!]", "Pagos Pendientes", stats['pagos_pendientes'], "#EAB308"),
            ("[€]", "Recaudado", f"{stats['dinero_recaudado']:.2f}€", "#22C55E"),
            ("[€]", "Pendiente", f"{stats['dinero_pendiente']:.2f}€", "#DC2626"),
        ]

        for i, (icono, titulo, valor, color) in enumerate(stats_data):
            self.crear_tarjeta_stat(grid_frame, icono, titulo, str(valor), color, i)

    def crear_tarjeta_stat(self, parent, icono, titulo, valor, color, indice):
        """Crea una tarjeta de estadística"""
        tarjeta = ctk.CTkFrame(parent, corner_radius=10, fg_color="#1a1a1a", border_width=2, border_color=color)
        tarjeta.grid(row=indice // 2, column=indice % 2, padx=15, pady=15, sticky="nsew")

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
            text=valor,
            font=("Arial", 28, "bold"),
            text_color=color
        ).pack(pady=(5, 15))

    def crear_tab_morosos(self, parent):
        """Crea la pestaña de usuarios morosos"""
        ctk.CTkLabel(
            parent,
            text="Usuarios con Pagos Pendientes",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        # Frame scrollable para morosos
        morosos_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        morosos_frame.pack(pady=10, padx=30, fill="both", expand=True)

        morosos = self.pago_model.obtener_morosos()

        if not morosos:
            ctk.CTkLabel(
                morosos_frame,
                text="¡Excelente! No hay usuarios con pagos pendientes",
                font=("Arial", 16),
                text_color="#22C55E"
            ).pack(pady=50)
        else:
            for usuario_id, nombre, pagos_pendientes, deuda_total in morosos:
                self.crear_tarjeta_moroso(morosos_frame, usuario_id, nombre, pagos_pendientes, deuda_total)

    def crear_tarjeta_moroso(self, parent, usuario_id, nombre, pagos_pendientes, deuda_total):
        """Crea una tarjeta para un usuario moroso"""
        tarjeta = ctk.CTkFrame(parent, corner_radius=10, border_width=2, border_color="#DC2626", fg_color="#1a1a1a")
        tarjeta.pack(pady=8, padx=10, fill="x")

        main_container = ctk.CTkFrame(tarjeta, fg_color="transparent")
        main_container.pack(fill="x", padx=20, pady=15)

        # Icono de alerta
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            left_frame,
            text="[!]",
            font=("Arial", 32),
            text_color="#DC2626"
        ).pack()

        # Información del usuario
        center_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        center_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            center_frame,
            text=f"Usuario: {nombre}",
            font=("Arial", 18, "bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            center_frame,
            text=f"Pagos pendientes: {pagos_pendientes}  |  Deuda total: {deuda_total:.2f}€",
            font=("Arial", 14),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(5, 0))

        # Botón para ver detalles
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.pack(side="right")

        ctk.CTkButton(
            right_frame,
            text="Ver Detalles",
            command=lambda: self.ver_detalles_moroso(usuario_id, nombre),
            width=120,
            height=35,
            font=("Arial", 12, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C"
        ).pack()

    def ver_detalles_moroso(self, usuario_id, nombre):
        """Muestra los detalles de los pagos pendientes de un usuario"""
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Pagos Pendientes - {nombre}")
        ventana.geometry("600x500")
        ventana.transient(self)
        ventana.grab_set()

        # Centrar
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - 300
        y = (ventana.winfo_screenheight() // 2) - 250
        ventana.geometry(f'600x500+{x}+{y}')

        ctk.CTkLabel(
            ventana,
            text=f"Pagos Pendientes de {nombre}",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # Frame scrollable
        pagos_frame = ctk.CTkScrollableFrame(ventana, fg_color="transparent")
        pagos_frame.pack(pady=10, padx=30, fill="both", expand=True)

        pagos_pendientes = self.pago_model.obtener_pagos_pendientes_usuario(usuario_id)

        for pago_id, mes, anio, monto in pagos_pendientes:
            pago_container = ctk.CTkFrame(pagos_frame, corner_radius=10, fg_color="#1a1a1a")
            pago_container.pack(pady=5, padx=10, fill="x")

            info_frame = ctk.CTkFrame(pago_container, fg_color="transparent")
            info_frame.pack(fill="x", padx=15, pady=12)

            nombre_mes = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                          "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes]

            ctk.CTkLabel(
                info_frame,
                text=f"{nombre_mes} {anio}",
                font=("Arial", 16, "bold"),
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                info_frame,
                text=f"{monto:.2f}€",
                font=("Arial", 16, "bold"),
                text_color="#EAB308"
            ).pack(side="right", padx=10)

        ctk.CTkButton(
            ventana,
            text="Cerrar",
            command=ventana.destroy,
            width=150,
            height=40,
            font=("Arial", 14, "bold")
        ).pack(pady=20)

    def crear_tab_generar_recibos(self, parent):
        """Crea la pestaña para generar recibos"""
        ctk.CTkLabel(
            parent,
            text="Generar Recibos Mensuales",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        info_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="#1a1a1a")
        info_frame.pack(pady=20, padx=50, fill="x")

        ctk.CTkLabel(
            info_frame,
            text="Generación Automática de Recibos",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        ctk.CTkLabel(
            info_frame,
            text="Genera recibos mensuales para todos los usuarios.\nCuota: 50€/mes\n\nSe generarán recibos de los últimos 3 meses para demostración.",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=10)

        # Mes y año actual
        ahora = datetime.now()
        nombre_mes = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][ahora.month]

        ctk.CTkLabel(
            info_frame,
            text=f"Mes actual: {nombre_mes} {ahora.year}",
            font=("Arial", 16, "bold"),
            text_color="#0EA5E9"
        ).pack(pady=10)

        ctk.CTkButton(
            info_frame,
            text="Generar Recibos del Mes Actual",
            command=self.generar_recibos_mes,
            width=300,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#22C55E",
            hover_color="#16A34A"
        ).pack(pady=20)

        self.resultado_label = ctk.CTkLabel(
            parent,
            text="",
            font=("Arial", 14),
            text_color="#22C55E"
        )
        self.resultado_label.pack(pady=10)

    def generar_recibos_mes(self):
        """Genera los recibos del mes actual para todos los usuarios"""
        # Generar también recibos de ejemplo
        recibos_generados = self.pago_model.generar_recibos_ejemplo()
        
        if recibos_generados > 0:
            self.resultado_label.configure(
                text=f"[OK] Se generaron {recibos_generados} recibos exitosamente",
                text_color="#22C55E"
            )
            # Actualizar vista de administrador
            self.after(1000, lambda: [self.destroy(), PagosView(self.master, self.usuario_id, True)])
        else:
            self.resultado_label.configure(
                text="Los recibos ya fueron generados",
                text_color="#EAB308"
            )

    def crear_interfaz_usuario(self):
        """Interfaz para usuarios normales"""
        # Subtítulo
        ctk.CTkLabel(
            self,
            text="Gestiona tus pagos mensuales del gimnasio - Cuota: 50€/mes",
            font=("Arial", 16),
            text_color="gray"
        ).pack(pady=(0, 10))

        # Frame scrollable para pagos
        pagos_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", height=500)
        pagos_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Obtener pagos del usuario
        pagos = self.pago_model.obtener_pagos_usuario(self.usuario_id)

        if not pagos:
            # Si no hay pagos, mostrar mensaje y botón para generar ejemplos
            ctk.CTkLabel(
                pagos_frame,
                text="No tienes pagos registrados",
                font=("Arial", 18, "bold")
            ).pack(pady=20)
            
            ctk.CTkLabel(
                pagos_frame,
                text="El sistema genera recibos mensuales automáticamente",
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=10)
        else:
            # Resumen
            pendientes = sum(1 for p in pagos if p[4] == 0)  # pagado == 0
            deuda_total = sum(p[3] for p in pagos if p[4] == 0)  # monto si no pagado

            resumen_frame = ctk.CTkFrame(pagos_frame, corner_radius=10, fg_color="#1a1a1a")
            resumen_frame.pack(pady=10, padx=10, fill="x")

            ctk.CTkLabel(
                resumen_frame,
                text=f"Resumen: {len(pagos)} recibos totales | {pendientes} pendientes | Deuda: {deuda_total:.2f}€",
                font=("Arial", 14, "bold")
            ).pack(pady=15)

            # Mostrar cada pago
            for pago in pagos:
                self.crear_tarjeta_pago(pagos_frame, pago)

    def crear_tarjeta_pago(self, parent, pago):
        """Crea una tarjeta para mostrar un pago"""
        pago_id, mes, anio, monto, pagado, fecha_pago = pago

        # Determinar color según estado
        if pagado:
            color_border = "#22C55E"
            icono = "[OK]"
            estado_texto = "PAGADO"
            color_estado = "#22C55E"
        else:
            color_border = "#DC2626"
            icono = "[!]"
            estado_texto = "PENDIENTE"
            color_estado = "#DC2626"

        # Nombre del mes
        nombre_mes = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][mes]

        tarjeta = ctk.CTkFrame(parent, corner_radius=10, border_width=2, border_color=color_border, fg_color="#1a1a1a")
        tarjeta.pack(pady=8, padx=10, fill="x")

        main_container = ctk.CTkFrame(tarjeta, fg_color="transparent")
        main_container.pack(fill="x", padx=20, pady=15)

        # Icono y estado
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

        # Información del pago
        center_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        center_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            center_frame,
            text=f"{nombre_mes} {anio}",
            font=("Arial", 18, "bold"),
            anchor="w"
        ).pack(fill="x")

        info_text = f"Monto: {monto:.2f}€"
        if pagado and fecha_pago:
            info_text += f"  |  Fecha de pago: {fecha_pago}"

        ctk.CTkLabel(
            center_frame,
            text=info_text,
            font=("Arial", 13),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(5, 0))

        # Botón para pagar (solo si no está pagado)
        if not pagado:
            right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
            right_frame.pack(side="right")

            ctk.CTkButton(
                right_frame,
                text="Pagar",
                command=lambda: self.pagar_recibo(pago_id),
                width=100,
                height=35,
                font=("Arial", 14, "bold"),
                fg_color="#22C55E",
                hover_color="#16A34A"
            ).pack()

    def pagar_recibo(self, pago_id):
        """Registra el pago de un recibo"""
        if self.pago_model.registrar_pago(pago_id):
            # Mostrar mensaje de éxito
            msg = ctk.CTkToplevel(self)
            msg.title("Pago Exitoso")
            msg.geometry("400x250")
            msg.transient(self)
            msg.grab_set()

            # Centrar
            msg.update_idletasks()
            x = (msg.winfo_screenwidth() // 2) - 200
            y = (msg.winfo_screenheight() // 2) - 125
            msg.geometry(f'400x250+{x}+{y}')

            ctk.CTkLabel(
                msg,
                text="[OK]",
                font=("Arial", 48),
                text_color="#22C55E"
            ).pack(pady=20)

            ctk.CTkLabel(
                msg,
                text="¡Pago registrado con éxito!",
                font=("Arial", 20, "bold")
            ).pack(pady=10)

            ctk.CTkLabel(
                msg,
                text="Tu recibo ha sido marcado como pagado",
                font=("Arial", 14),
                text_color="gray"
            ).pack(pady=5)

            ctk.CTkButton(
                msg,
                text="Aceptar",
                command=lambda: [msg.destroy(), self.destroy(), PagosView(self.master, self.usuario_id, self.es_admin)],
                width=150,
                height=40,
                font=("Arial", 14, "bold"),
                fg_color="#22C55E",
                hover_color="#16A34A"
            ).pack(pady=20)
        else:
            # Mostrar error
            pass
