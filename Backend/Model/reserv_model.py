import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.DataBase.database import Database
from mysql.connector import Error

class ReservaModel:
    def __init__(self):
        pass
    
    def crear_reserva(self, usuario_id, clase, fecha, hora, duracion=1):
        """Crea una nueva reserva en la base de datos"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO reservas (usuario_id, clase, fecha, hora, duracion) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (usuario_id, clase, fecha, hora, duracion)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Error al crear reserva: {e}")
            return False
    
    def marcar_asistencia(self, reserva_id):
        """Marca una reserva como asistida"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE reservas SET asistio = TRUE WHERE id = %s",
                (reserva_id,)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Error al marcar asistencia: {e}")
            return False
    
    def obtener_reservas_usuario(self, usuario_id):
        """Obtiene todas las reservas de un usuario"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT id, clase, fecha, hora, duracion, asistio 
                   FROM reservas WHERE usuario_id = %s 
                   ORDER BY fecha DESC, hora DESC""",
                (usuario_id,)
            )
            reservas = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return reservas
        except Error as e:
            print(f"Error al obtener reservas: {e}")
            return []
