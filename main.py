from Frontend.View.login import Login
from Backend.Controller.login_controller import LoginController

if __name__ == "__main__":
    controlador_login = LoginController(None)
    vista_login = Login(controlador_login)
    controlador_login.vista = vista_login
    vista_login.mainloop()
