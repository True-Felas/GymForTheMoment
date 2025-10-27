# Front/View/login.py
import customtkinter as ctk

class Login(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.title("Gimnasio - Iniciar Sesión")
        self.geometry("450x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Centrar ventana
        self.center_window()
        
        # Variable para alternar entre login y registro
        self.modo_registro = False
        
        self.crear_interfaz_login()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz_login(self):
        """Crea la interfaz de login/registro"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Título
        self.titulo = ctk.CTkLabel(
            self.main_frame, 
            text="Bienvenido al Gimnasio",
            font=("Arial", 28, "bold")
        )
        self.titulo.pack(pady=(0, 10))
        
        self.subtitulo = ctk.CTkLabel(
            self.main_frame,
            text="Inicia sesión para continuar",
            font=("Arial", 14)
        )
        self.subtitulo.pack(pady=(0, 30))
        
        # Frame del formulario
        form_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Usuario
        ctk.CTkLabel(
            form_frame,
            text="Usuario:",
            font=("Arial", 14, "bold")
        ).pack(pady=(30, 5), anchor="w", padx=30)
        
        self.usuario_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ingresa tu usuario",
            width=300,
            height=40,
            font=("Arial", 12)
        )
        self.usuario_entry.pack(pady=(0, 15), padx=30)
        
        # Contraseña
        ctk.CTkLabel(
            form_frame,
            text="Contraseña:",
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 5), anchor="w", padx=30)
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Ingresa tu contraseña",
            show="•",
            width=300,
            height=40,
            font=("Arial", 12)
        )
        self.password_entry.pack(pady=(0, 15), padx=30)
        
        # Confirmar contraseña (oculto inicialmente)
        self.label_confirmar = ctk.CTkLabel(
            form_frame,
            text="Confirmar Contraseña:",
            font=("Arial", 14, "bold")
        )
        
        self.confirmar_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Confirma tu contraseña",
            show="•",
            width=300,
            height=40,
            font=("Arial", 12)
        )
        
        # Label de error
        self.error_label = ctk.CTkLabel(
            form_frame,
            text="",
            text_color="red",
            font=("Arial", 12)
        )
        self.error_label.pack(pady=10)
        
        # Botón principal (Login/Registro)
        self.boton_principal = ctk.CTkButton(
            form_frame,
            text="Iniciar Sesión",
            command=self.intentar_login,
            width=300,
            height=45,
            font=("Arial", 16, "bold"),
            fg_color="#0284C7",
            hover_color="#0369A1"
        )
        self.boton_principal.pack(pady=15, padx=30)
        
        # Separador
        ctk.CTkLabel(
            form_frame,
            text="────────  o  ────────",
            font=("Arial", 12)
        ).pack(pady=10)
        
        # Botón para cambiar entre login y registro
        self.boton_cambiar = ctk.CTkButton(
            form_frame,
            text="¿No tienes cuenta? Regístrate",
            command=self.cambiar_modo,
            width=300,
            height=40,
            font=("Arial", 14),
            fg_color="transparent",
            hover_color="#1E293B",
            border_width=2
        )
        self.boton_cambiar.pack(pady=(0, 30), padx=30)
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.intentar_accion())
        self.usuario_entry.bind("<Return>", lambda e: self.password_entry.focus())
    
    def cambiar_modo(self):
        """Alterna entre modo login y registro"""
        self.modo_registro = not self.modo_registro
        self.error_label.configure(text="")
        
        if self.modo_registro:
            # Cambiar a modo registro
            self.subtitulo.configure(text="Crea tu cuenta nueva")
            self.boton_principal.configure(
                text="Registrarse",
                command=self.intentar_registro
            )
            self.boton_cambiar.configure(text="¿Ya tienes cuenta? Inicia sesión")
            
            # Mostrar campo de confirmar contraseña
            self.label_confirmar.pack(pady=(5, 5), anchor="w", padx=30, before=self.error_label)
            self.confirmar_entry.pack(pady=(0, 15), padx=30, before=self.error_label)
            self.confirmar_entry.bind("<Return>", lambda e: self.intentar_registro())
            
        else:
            # Cambiar a modo login
            self.subtitulo.configure(text="Inicia sesión para continuar")
            self.boton_principal.configure(
                text="Iniciar Sesión",
                command=self.intentar_login
            )
            self.boton_cambiar.configure(text="¿No tienes cuenta? Regístrate")
            
            # Ocultar campo de confirmar contraseña
            self.label_confirmar.pack_forget()
            self.confirmar_entry.pack_forget()
            self.password_entry.bind("<Return>", lambda e: self.intentar_login())
    
    def intentar_login(self):
        """Intenta iniciar sesión"""
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()
        self.controller.validar_login(usuario, password)
    
    def intentar_registro(self):
        """Intenta registrar un nuevo usuario"""
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()
        confirmar = self.confirmar_entry.get()
        
        exito, mensaje = self.controller.registrar_usuario(usuario, password, confirmar)
        
        if exito:
            self.mostrar_exito(mensaje)
            # Limpiar campos
            self.usuario_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirmar_entry.delete(0, 'end')
            # Cambiar a modo login después de 2 segundos
            self.after(2000, self.cambiar_modo)
        else:
            self.mostrar_error(mensaje)
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        self.error_label.configure(text=mensaje, text_color="red")
    
    def mostrar_exito(self, mensaje):
        """Muestra un mensaje de éxito"""
        self.error_label.configure(text=mensaje, text_color="green")