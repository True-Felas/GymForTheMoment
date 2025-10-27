import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.DataBase.database import Database
from mysql.connector import Error

class UserModel:
    def __init__(self):
        # Asegurar que la base de datos esté inicializada
        db = Database()
        db.cerrar()
        self._insertar_usuarios_ejemplo()
    
    def _insertar_usuarios_ejemplo(self):
        """Inserta usuarios de ejemplo si no existen"""
        usuarios_ejemplo = [
            ("admin", "1234"),
            ("juan", "gym2025"),
            ("sofia", "fitlife")
        ]
        
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            for nombre, password in usuarios_ejemplo:
                try:
                    cursor.execute(
                        "INSERT INTO usuarios (nombre, password) VALUES (%s, %s)",
                        (nombre, password)
                    )
                    conn.commit()
                except Error:
                    pass  # Usuario ya existe
            
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Error al insertar usuarios de ejemplo: {e}")

    def validar_usuario(self, nombre, password):
        """Valida el usuario contra la base de datos"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id FROM usuarios WHERE nombre = %s AND password = %s",
                (nombre, password)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return result is not None
        except Error as e:
            print(f"Error al validar usuario: {e}")
            return False
    
    def registrar_usuario(self, nombre, password):
        """Registra un nuevo usuario en la base de datos"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute(
                "SELECT id FROM usuarios WHERE nombre = %s",
                (nombre,)
            )
            
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False, "El usuario ya existe"
            
            # Insertar nuevo usuario
            cursor.execute(
                "INSERT INTO usuarios (nombre, password, nivel) VALUES (%s, %s, 1)",
                (nombre, password)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True, "Usuario registrado exitosamente"
            
        except Error as e:
            print(f"Error al registrar usuario: {e}")
            return False, f"Error al registrar: {str(e)}"
    
    def obtener_id_usuario(self, nombre):
        """Obtiene el ID del usuario"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id FROM usuarios WHERE nombre = %s",
                (nombre,)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return result[0] if result else None
        except Error as e:
            print(f"Error al obtener ID de usuario: {e}")
            return None
    
    def obtener_estadisticas(self, usuario_id):
        """Obtiene las estadísticas del usuario desde la base de datos"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Total de reservas
            cursor.execute(
                "SELECT COUNT(*) FROM reservas WHERE usuario_id = %s",
                (usuario_id,)
            )
            total_reservas = cursor.fetchone()[0]
            
            # Horas entrenadas (suma de duraciones de clases asistidas)
            cursor.execute(
                "SELECT SUM(duracion) FROM reservas WHERE usuario_id = %s AND asistio = TRUE",
                (usuario_id,)
            )
            horas_entrenadas = cursor.fetchone()[0] or 0
            
            # Clases asistidas
            cursor.execute(
                "SELECT COUNT(*) FROM reservas WHERE usuario_id = %s AND asistio = TRUE",
                (usuario_id,)
            )
            clases_asistidas = cursor.fetchone()[0]
            
            # Nivel del usuario
            cursor.execute(
                "SELECT nivel FROM usuarios WHERE id = %s",
                (usuario_id,)
            )
            nivel = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return {
                'reservas': total_reservas,
                'horas': horas_entrenadas,
                'clases': clases_asistidas,
                'nivel': nivel
            }
        except Error as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'reservas': 0,
                'horas': 0,
                'clases': 0,
                'nivel': 1
            }
