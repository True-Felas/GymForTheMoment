class UserModel:
    def __init__(self):
        # Diccionario de ejemplo (usuario: contraseña)
        self.usuarios = {
            "admin": "1234",
            "juan": "gym2025",
            "sofia": "fitlife"
        }

    def validar_usuario(self, nombre, password):
        return self.usuarios.get(nombre) == password
