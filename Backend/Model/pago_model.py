import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.DataBase.database import Database
import sqlite3
from datetime import datetime


class PagoModel:
    """Modelo para gestionar pagos mensuales del gimnasio"""
    
    # Cuota mensual del gimnasio
    CUOTA_MENSUAL = 50.0  # €50 por mes
    
    def __init__(self):
        pass
    
    def generar_recibo_mensual(self, usuario_id, mes, anio):
        """Genera un recibo mensual para un usuario si no existe"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Verificar si ya existe un recibo para este mes
            cursor.execute(
                "SELECT id FROM pagos WHERE usuario_id = ? AND mes = ? AND anio = ?",
                (usuario_id, mes, anio)
            )
            
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False  # Ya existe
            
            # Crear nuevo recibo
            cursor.execute(
                """INSERT INTO pagos (usuario_id, mes, anio, monto, pagado) 
                   VALUES (?, ?, ?, ?, 0)""",
                (usuario_id, mes, anio, self.CUOTA_MENSUAL)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al generar recibo mensual: {e}")
            return False
    
    def registrar_pago(self, pago_id):
        """Registra el pago de un recibo"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute(
                "UPDATE pagos SET pagado = 1, fecha_pago = ? WHERE id = ?",
                (fecha_actual, pago_id)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar pago: {e}")
            return False
    
    def obtener_pagos_usuario(self, usuario_id):
        """Obtiene todos los pagos de un usuario"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT id, mes, anio, monto, pagado, fecha_pago 
                   FROM pagos 
                   WHERE usuario_id = ? 
                   ORDER BY anio DESC, mes DESC""",
                (usuario_id,)
            )
            pagos = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return pagos
        except sqlite3.Error as e:
            print(f"Error al obtener pagos del usuario: {e}")
            return []
    
    def obtener_morosos(self):
        """Obtiene la lista de usuarios con pagos pendientes (morosos)"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT DISTINCT u.id, u.nombre, COUNT(p.id) as pagos_pendientes, 
                          SUM(p.monto) as deuda_total
                   FROM usuarios u
                   INNER JOIN pagos p ON u.id = p.usuario_id
                   WHERE p.pagado = 0
                   GROUP BY u.id, u.nombre
                   ORDER BY deuda_total DESC"""
            )
            morosos = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return morosos
        except sqlite3.Error as e:
            print(f"Error al obtener morosos: {e}")
            return []
    
    def obtener_pagos_pendientes_usuario(self, usuario_id):
        """Obtiene los pagos pendientes de un usuario específico"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT id, mes, anio, monto 
                   FROM pagos 
                   WHERE usuario_id = ? AND pagado = 0 
                   ORDER BY anio ASC, mes ASC""",
                (usuario_id,)
            )
            pagos_pendientes = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return pagos_pendientes
        except sqlite3.Error as e:
            print(f"Error al obtener pagos pendientes: {e}")
            return []
    
    def generar_recibos_automaticos(self):
        """Genera recibos mensuales para todos los usuarios activos (mes actual)"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Obtener todos los usuarios
            cursor.execute("SELECT id FROM usuarios")
            usuarios = cursor.fetchall()
            
            # Obtener mes y año actual
            ahora = datetime.now()
            mes_actual = ahora.month
            anio_actual = ahora.year
            
            recibos_generados = 0
            for (usuario_id,) in usuarios:
                if self.generar_recibo_mensual(usuario_id, mes_actual, anio_actual):
                    recibos_generados += 1
            
            cursor.close()
            conn.close()
            
            return recibos_generados
        except sqlite3.Error as e:
            print(f"Error al generar recibos automáticos: {e}")
            return 0
    
    def obtener_estadisticas_pagos(self):
        """Obtiene estadísticas generales de pagos"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Total de recibos generados
            cursor.execute("SELECT COUNT(*) FROM pagos")
            total_recibos = cursor.fetchone()[0]
            
            # Total de pagos realizados
            cursor.execute("SELECT COUNT(*) FROM pagos WHERE pagado = 1")
            pagos_realizados = cursor.fetchone()[0]
            
            # Total de pagos pendientes
            cursor.execute("SELECT COUNT(*) FROM pagos WHERE pagado = 0")
            pagos_pendientes = cursor.fetchone()[0]
            
            # Dinero recaudado
            cursor.execute("SELECT SUM(monto) FROM pagos WHERE pagado = 1")
            dinero_recaudado = cursor.fetchone()[0] or 0
            
            # Dinero pendiente
            cursor.execute("SELECT SUM(monto) FROM pagos WHERE pagado = 0")
            dinero_pendiente = cursor.fetchone()[0] or 0
            
            cursor.close()
            conn.close()
            
            return {
                'total_recibos': total_recibos,
                'pagos_realizados': pagos_realizados,
                'pagos_pendientes': pagos_pendientes,
                'dinero_recaudado': dinero_recaudado,
                'dinero_pendiente': dinero_pendiente
            }
        except sqlite3.Error as e:
            print(f"Error al obtener estadísticas de pagos: {e}")
            return {
                'total_recibos': 0,
                'pagos_realizados': 0,
                'pagos_pendientes': 0,
                'dinero_recaudado': 0,
                'dinero_pendiente': 0
            }
