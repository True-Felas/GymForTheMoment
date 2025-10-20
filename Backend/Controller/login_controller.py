# Front/Controller/login_controller.py
from Backend.Model.user_model import UserModel
from Frontend.View.app import App

class LoginController:
    def __init__(self, vista_login):
        self.vista = vista_login
        self.modelo = UserModel()

    def validar_login(self, usuario, password):
        if self.modelo.validar_usuario(usuario, password):
            self.abrir_app()
        else:
            self.vista.mostrar_error("Usuario o contraseña incorrectos")

    def abrir_app(self):
        self.vista.destroy()  # Cierra ventana de login
        app_window = App()  # Crea instancia de la ventana principal
        app_window.mainloop()  # Ejecuta la app
