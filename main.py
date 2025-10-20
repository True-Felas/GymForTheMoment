from Frontend.View.login import Login
from Backend.Controller.login_controller import LoginController

if __name__ == "__main__":
    controlador_login = LoginController(None)
    vista_login = Login(controlador_login)
    controlador_login.vista = vista_login
    # ==== Metodo para intentar login ====
    def intentar_login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        self.controller.intentar_login(usuario, password)

    def mostrar_error(self, mensaje):
        self.error_label.configure(text=mensaje)

    vista_login.mainloop()
