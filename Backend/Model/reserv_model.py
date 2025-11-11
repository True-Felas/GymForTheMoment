import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.DataBase.database import Database
import sqlite3
from datetime import datetime

class ReservaModel:
    # Configuración
    CAPACIDAD_POR_MAQUINA = 1  # Solo una persona por máquina
    
    # Horarios disponibles del gimnasio (24 horas)
    HORARIOS_DISPONIBLES = [
        "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
    ]
    
    # Máquinas disponibles en el gimnasio
    MAQUINAS_DISPONIBLES = [
        "Cinta de Correr 1",
        "Cinta de Correr 2",
        "Bicicleta Estática 1",
        "Bicicleta Estática 2",
        "Elíptica 1",
        "Elíptica 2",
        "Remo 1",
        "Press de Banca",
        "Prensa de Piernas",
        "Máquina de Poleas",
        "Rack de Sentadillas",
        "Banco de Abdominales"
    ]
    
    def __init__(self):
        pass
    
    def crear_reserva(self, usuario_id, maquina, fecha, hora, duracion=1):
        """Crea una nueva reserva en la base de datos"""
        try:
            # Verificar si la máquina está disponible en ese horario
            if not self.maquina_disponible(fecha, maquina, hora):
                print("La máquina no está disponible en ese horario")
                return False
            
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO reservas (usuario_id, maquina, fecha, hora, duracion) 
                   VALUES (?, ?, ?, ?, ?)""",
                (usuario_id, maquina, fecha, hora, duracion)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al crear reserva: {e}")
            return False
    
    def marcar_completada(self, reserva_id):
        """Marca una reserva como completada"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE reservas SET completada = 1 WHERE id = ?",
                (reserva_id,)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al marcar como completada: {e}")
            return False
    
    def obtener_reservas_usuario(self, usuario_id):
        """Obtiene todas las reservas de un usuario"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT id, maquina, fecha, hora, duracion, completada 
                   FROM reservas WHERE usuario_id = ? 
                   ORDER BY fecha DESC, hora DESC""",
                (usuario_id,)
            )
            reservas = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return reservas
        except sqlite3.Error as e:
            print(f"Error al obtener reservas: {e}")
            return []
    
    def verificar_maquina_ocupada(self, fecha, maquina, hora):
        """Verifica si una máquina está ocupada en un horario específico"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT COUNT(*) FROM reservas 
                   WHERE fecha = ? AND maquina = ? AND hora = ?""",
                (fecha, maquina, hora)
            )
            resultado = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return (resultado[0] if resultado else 0) > 0
        except sqlite3.Error as e:
            print(f"Error al verificar máquina: {e}")
            return True  # Por seguridad, asumir que está ocupada
    
    def maquina_disponible(self, fecha, maquina, hora):
        """Verifica si una máquina está disponible (no ocupada)"""
        return not self.verificar_maquina_ocupada(fecha, maquina, hora)
    
    def obtener_info_maquinas(self, fecha, hora):
        """
        Obtiene información de todas las máquinas para una fecha y hora específica.
        Retorna un diccionario con: maquina, disponible
        """
        info_maquinas = []
        
        for maquina in self.MAQUINAS_DISPONIBLES:
            disponible = self.maquina_disponible(fecha, maquina, hora)
            
            info_maquinas.append({
                'maquina': maquina,
                'disponible': disponible
            })
        
        return info_maquinas
    
    def obtener_info_horarios_maquina(self, fecha, maquina):
        """
        Obtiene información de todos los horarios para una fecha y máquina específica.
        Retorna un diccionario con: hora, disponible
        """
        info_horarios = []
        
        for hora in self.HORARIOS_DISPONIBLES:
            disponible = self.maquina_disponible(fecha, maquina, hora)
            
            info_horarios.append({
                'hora': hora,
                'disponible': disponible
            })
        
        return info_horarios
    
    def procesar_reservas_vencidas(self):
        """
        Verifica y marca como completadas las reservas cuyo horario ya pasó.
        Retorna una lista de usuarios que completaron reservas.
        """
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Obtener fecha y hora actual
            ahora = datetime.now()
            fecha_actual = ahora.strftime('%Y-%m-%d')
            hora_actual = ahora.strftime('%H:00')
            
            # Buscar reservas no completadas cuya fecha/hora ya pasó
            cursor.execute(
                """SELECT id, usuario_id FROM reservas 
                   WHERE completada = 0 
                   AND (fecha < ? OR (fecha = ? AND hora < ?))""",
                (fecha_actual, fecha_actual, hora_actual)
            )
            reservas_vencidas = cursor.fetchall()
            
            usuarios_afectados = []
            
            for reserva_id, usuario_id in reservas_vencidas:
                # Marcar como completada
                cursor.execute(
                    "UPDATE reservas SET completada = 1 WHERE id = ?",
                    (reserva_id,)
                )
                usuarios_afectados.append(usuario_id)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return usuarios_afectados
            
        except sqlite3.Error as e:
            print(f"Error al procesar reservas vencidas: {e}")
            return []
