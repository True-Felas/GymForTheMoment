# Front/View/login.py
import customtkinter as ctk

class Login(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Login - Gimnasio")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ==== Título ====
        titulo = ctk.CTkLabel(self, text="Iniciar Sesión", font=("Arial", 24, "bold"))
        titulo.pack(pady=20)

        # ==== Campos de entrada ====
        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.usuario_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=10)

        # ==== Botón de login ====
        login_btn = ctk.CTkButton(self, text="Ingresar", command=self.intentar_login)
        login_btn.pack(pady=20)

        # Mensaje de error
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack()

    # ==== Metodo para intentar login ====
    def intentar_login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        if self.controller.validar_login(usuario, password):
            self.destroy()  # Cerrar ventana de login
            self.controller.abrir_app()  # Abrir ventana principal
        else:
            self.error_label.configure(text="Usuario o contraseña incorrectos")