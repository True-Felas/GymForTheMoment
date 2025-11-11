import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.DataBase.database import Database
import sqlite3

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
                        "INSERT INTO usuarios (nombre, password) VALUES (?, ?)",
                        (nombre, password)
                    )
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass  # Usuario ya existe
            
            cursor.close()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al insertar usuarios de ejemplo: {e}")

    def validar_usuario(self, nombre, password):
        """Valida el usuario contra la base de datos"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id FROM usuarios WHERE nombre = ? AND password = ?",
                (nombre, password)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return result is not None
        except sqlite3.Error as e:
            print(f"Error al validar usuario: {e}")
            return False
    
    def registrar_usuario(self, nombre, password):
        """Registra un nuevo usuario en la base de datos"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute(
                "SELECT id FROM usuarios WHERE nombre = ?",
                (nombre,)
            )
            
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False, "El usuario ya existe"
            
            # Insertar nuevo usuario
            cursor.execute(
                "INSERT INTO usuarios (nombre, password, nivel, reservas_completadas) VALUES (?, ?, 1, 0)",
                (nombre, password)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True, "Usuario registrado exitosamente"
            
        except sqlite3.Error as e:
            print(f"Error al registrar usuario: {e}")
            return False, f"Error al registrar: {str(e)}"
    
    def obtener_id_usuario(self, nombre):
        """Obtiene el ID del usuario"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id FROM usuarios WHERE nombre = ?",
                (nombre,)
            )
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error al obtener ID de usuario: {e}")
            return None
    
    def obtener_estadisticas(self, usuario_id):
        """Obtiene las estadísticas del usuario desde la base de datos"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Total de reservas
            cursor.execute(
                "SELECT COUNT(*) FROM reservas WHERE usuario_id = ?",
                (usuario_id,)
            )
            total_reservas = cursor.fetchone()[0]
            
            # Horas entrenadas (suma de duraciones de reservas completadas)
            cursor.execute(
                "SELECT SUM(duracion) FROM reservas WHERE usuario_id = ? AND completada = 1",
                (usuario_id,)
            )
            horas_entrenadas = cursor.fetchone()[0] or 0
            
            # Reservas completadas
            cursor.execute(
                "SELECT COUNT(*) FROM reservas WHERE usuario_id = ? AND completada = 1",
                (usuario_id,)
            )
            reservas_completadas = cursor.fetchone()[0]
            
            # Nivel del usuario y reservas completadas
            cursor.execute(
                "SELECT nivel, reservas_completadas FROM usuarios WHERE id = ?",
                (usuario_id,)
            )
            result = cursor.fetchone()
            nivel = result[0] if result else 1
            reservas_para_nivel = result[1] if result else 0
            
            cursor.close()
            conn.close()
            
            return {
                'reservas': total_reservas,
                'horas': horas_entrenadas,
                'reservas_completadas': reservas_completadas,
                'nivel': nivel,
                'reservas_para_nivel': reservas_para_nivel
            }
        except sqlite3.Error as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'reservas': 0,
                'horas': 0,
                'reservas_completadas': 0,
                'nivel': 1,
                'reservas_para_nivel': 0
            }
    
    def incrementar_reservas_completadas(self, usuario_id):
        """Incrementa el contador de reservas completadas y sube de nivel si es necesario"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Obtener reservas completadas actuales
            cursor.execute(
                "SELECT reservas_completadas, nivel FROM usuarios WHERE id = ?",
                (usuario_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                cursor.close()
                conn.close()
                return
            
            reservas_completadas = result[0]
            nivel_actual = result[1]
            
            # Incrementar contador
            nuevas_reservas = reservas_completadas + 1
            
            # Cada 3 reservas completadas, sube de nivel
            nuevo_nivel = nivel_actual
            if nuevas_reservas % 3 == 0:
                nuevo_nivel = nivel_actual + 1
                print(f"¡Usuario {usuario_id} ha subido al nivel {nuevo_nivel}!")
            
            # Actualizar en la base de datos
            cursor.execute(
                "UPDATE usuarios SET reservas_completadas = ?, nivel = ? WHERE id = ?",
                (nuevas_reservas, nuevo_nivel, usuario_id)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Error al incrementar reservas completadas: {e}")
