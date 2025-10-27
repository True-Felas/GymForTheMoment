# Front/Controller/login_controller.py
from Backend.Model.user_model import UserModel
from Frontend.View.app import App

class LoginController:
    def __init__(self, vista_login):
        self.vista = vista_login
        self.modelo = UserModel()
        self.usuario_actual = None

    def validar_login(self, usuario, password):
        if not usuario or not password:
            self.vista.mostrar_error("Por favor, completa todos los campos")
            return
            
        if self.modelo.validar_usuario(usuario, password):
            self.usuario_actual = usuario
            self.abrir_app()
        else:
            self.vista.mostrar_error("Usuario o contraseña incorrectos")

    def registrar_usuario(self, usuario, password, confirmar_password):
        # Validaciones
        if not usuario or not password or not confirmar_password:
            return False, "Por favor, completa todos los campos"
        
        if len(usuario) < 3:
            return False, "El usuario debe tener al menos 3 caracteres"
        
        if len(password) < 4:
            return False, "La contraseña debe tener al menos 4 caracteres"
        
        if password != confirmar_password:
            return False, "Las contraseñas no coinciden"
        
        # Intentar registrar
        exito, mensaje = self.modelo.registrar_usuario(usuario, password)
        return exito, mensaje

    def abrir_app(self):
        usuario_id = self.modelo.obtener_id_usuario(self.usuario_actual)
        self.vista.destroy()  # Cierra ventana de login
        app_window = App(usuario_id, self.usuario_actual)  # Pasa el ID y nombre del usuario
        app_window.mainloop()  # Ejecuta la app
