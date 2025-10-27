import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.DataBase.database import Database
from mysql.connector import Error

class ReservaModel:
    # Configuración
    CAPACIDAD_MAXIMA = 10  # Máximo de personas por clase
    
    # Horarios disponibles del gimnasio
    HORARIOS_DISPONIBLES = [
        "08:00", "09:00", "10:00", "11:00", "12:00",
        "13:00", "14:00", "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00", "21:00"
    ]
    
    # Tipos de clases disponibles
    CLASES_DISPONIBLES = [
        "Yoga",
        "Spinning",
        "Crossfit",
        "Pilates",
        "Zumba",
        "Body Combat",
        "GAP",
        "Cardio Box"
    ]
    
    def __init__(self):
        pass
    
    def crear_reserva(self, usuario_id, clase, fecha, hora, duracion=1):
        """Crea una nueva reserva en la base de datos"""
        try:
            # Verificar si hay cupo disponible
            if not self.hay_cupo_disponible(fecha, clase, hora):
                print("No hay cupo disponible para esta clase")
                return False
            
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
    
    def contar_reservas_por_horario(self, fecha, clase, hora):
        """Cuenta cuántas personas han reservado para un horario específico"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT COUNT(*) FROM reservas 
                   WHERE fecha = %s AND clase = %s AND hora = %s""",
                (fecha, clase, hora)
            )
            resultado = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return resultado[0] if resultado else 0
        except Error as e:
            print(f"Error al contar reservas: {e}")
            return 0
    
    def hay_cupo_disponible(self, fecha, clase, hora):
        """Verifica si hay cupo disponible para un horario específico"""
        reservas_actuales = self.contar_reservas_por_horario(fecha, clase, hora)
        return reservas_actuales < self.CAPACIDAD_MAXIMA
    
    def obtener_info_horarios(self, fecha, clase):
        """
        Obtiene información detallada de todos los horarios para una fecha y clase.
        Retorna un diccionario con: hora, reservas, capacidad_maxima, disponible, porcentaje
        """
        info_horarios = []
        
        for hora in self.HORARIOS_DISPONIBLES:
            reservas = self.contar_reservas_por_horario(fecha, clase, hora)
            disponible = reservas < self.CAPACIDAD_MAXIMA
            cupos_disponibles = self.CAPACIDAD_MAXIMA - reservas
            porcentaje_ocupacion = (reservas / self.CAPACIDAD_MAXIMA) * 100
            
            info_horarios.append({
                'hora': hora,
                'reservas': reservas,
                'capacidad_maxima': self.CAPACIDAD_MAXIMA,
                'cupos_disponibles': cupos_disponibles,
                'disponible': disponible,
                'porcentaje_ocupacion': porcentaje_ocupacion
            })
        
        return info_horarios
