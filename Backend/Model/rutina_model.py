import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Backend.DataBase.database import Database
import sqlite3


class RutinaModel:
    """Modelo para gestionar rutinas de ejercicios"""
    
    # Definición de rutinas por nivel
    RUTINAS = {
        "facil": {
            "nombre": "Rutina Principiante",
            "descripcion": "Perfecta para comenzar tu viaje fitness",
            "duracion": "30-45 min",
            "ejercicios": [
                {"nombre": "Sentadillas", "series": 3, "repeticiones": 10, "descanso": "60s"},
                {"nombre": "Flexiones de rodillas", "series": 3, "repeticiones": 8, "descanso": "60s"},
                {"nombre": "Plancha", "series": 3, "repeticiones": "20s", "descanso": "45s"},
                {"nombre": "Crunches abdominales", "series": 3, "repeticiones": 12, "descanso": "45s"},
                {"nombre": "Elevaciones de pantorrilla", "series": 3, "repeticiones": 15, "descanso": "45s"},
                {"nombre": "Puente de glúteos", "series": 3, "repeticiones": 12, "descanso": "45s"},
                {"nombre": "Superman", "series": 3, "repeticiones": 10, "descanso": "45s"},
            ]
        },
        "intermedio": {
            "nombre": "Rutina Intermedia",
            "descripcion": "Para quienes ya tienen una base sólida",
            "duracion": "45-60 min",
            "ejercicios": [
                {"nombre": "Sentadillas con peso", "series": 4, "repeticiones": 12, "descanso": "90s"},
                {"nombre": "Press de banca", "series": 4, "repeticiones": 10, "descanso": "90s"},
                {"nombre": "Peso muerto", "series": 4, "repeticiones": 8, "descanso": "120s"},
                {"nombre": "Dominadas asistidas", "series": 3, "repeticiones": 8, "descanso": "90s"},
                {"nombre": "Fondos en paralelas", "series": 3, "repeticiones": 10, "descanso": "90s"},
                {"nombre": "Remo con barra", "series": 4, "repeticiones": 10, "descanso": "90s"},
                {"nombre": "Plancha lateral", "series": 3, "repeticiones": "30s", "descanso": "60s"},
                {"nombre": "Zancadas con mancuernas", "series": 3, "repeticiones": 12, "descanso": "75s"},
            ]
        },
        "dificil": {
            "nombre": "Rutina Avanzada",
            "descripcion": "Para atletas experimentados",
            "duracion": "60-90 min",
            "ejercicios": [
                {"nombre": "Sentadillas búlgaras", "series": 4, "repeticiones": 10, "descanso": "120s"},
                {"nombre": "Press militar con barra", "series": 4, "repeticiones": 8, "descanso": "120s"},
                {"nombre": "Peso muerto rumano", "series": 4, "repeticiones": 10, "descanso": "120s"},
                {"nombre": "Dominadas con peso", "series": 4, "repeticiones": 8, "descanso": "120s"},
                {"nombre": "Fondos en anillas", "series": 4, "repeticiones": 10, "descanso": "120s"},
                {"nombre": "Muscle-ups", "series": 3, "repeticiones": 5, "descanso": "180s"},
                {"nombre": "Front squat", "series": 4, "repeticiones": 8, "descanso": "120s"},
                {"nombre": "Pistol squats", "series": 3, "repeticiones": 6, "descanso": "90s"},
                {"nombre": "Handstand push-ups", "series": 3, "repeticiones": 8, "descanso": "120s"},
                {"nombre": "Dragon flag", "series": 3, "repeticiones": 6, "descanso": "90s"},
            ]
        }
    }
    
    def __init__(self):
        self._crear_tabla_rutinas()
    
    def _crear_tabla_rutinas(self):
        """Crea la tabla de rutinas completadas si no existe"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rutinas_completadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    nivel TEXT NOT NULL,
                    fecha_completada TEXT NOT NULL,
                    ejercicios_completados INTEGER DEFAULT 0,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
            cursor.close()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al crear tabla de rutinas: {e}")
    
    def obtener_rutina(self, nivel):
        """Obtiene la rutina para un nivel específico"""
        return self.RUTINAS.get(nivel, None)
    
    def obtener_todas_rutinas(self):
        """Obtiene todas las rutinas disponibles"""
        return self.RUTINAS
    
    def marcar_rutina_completada(self, usuario_id, nivel, ejercicios_completados):
        """Marca una rutina como completada"""
        try:
            from datetime import datetime
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute(
                """INSERT INTO rutinas_completadas 
                   (usuario_id, nivel, fecha_completada, ejercicios_completados) 
                   VALUES (?, ?, ?, ?)""",
                (usuario_id, nivel, fecha_actual, ejercicios_completados)
            )
            conn.commit()
            
            cursor.close()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error al marcar rutina completada: {e}")
            return False
    
    def obtener_rutinas_completadas(self, usuario_id):
        """Obtiene todas las rutinas completadas por un usuario"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT nivel, fecha_completada, ejercicios_completados 
                   FROM rutinas_completadas 
                   WHERE usuario_id = ? 
                   ORDER BY fecha_completada DESC""",
                (usuario_id,)
            )
            rutinas = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return rutinas
        except sqlite3.Error as e:
            print(f"Error al obtener rutinas completadas: {e}")
            return []
    
    def obtener_estadisticas_rutinas(self, usuario_id):
        """Obtiene estadísticas de rutinas del usuario"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            # Total de rutinas completadas
            cursor.execute(
                "SELECT COUNT(*) FROM rutinas_completadas WHERE usuario_id = ?",
                (usuario_id,)
            )
            total_rutinas = cursor.fetchone()[0]
            
            # Rutinas por nivel
            cursor.execute(
                """SELECT nivel, COUNT(*) 
                   FROM rutinas_completadas 
                   WHERE usuario_id = ? 
                   GROUP BY nivel""",
                (usuario_id,)
            )
            por_nivel = dict(cursor.fetchall())
            
            # Total de ejercicios completados
            cursor.execute(
                "SELECT SUM(ejercicios_completados) FROM rutinas_completadas WHERE usuario_id = ?",
                (usuario_id,)
            )
            total_ejercicios = cursor.fetchone()[0] or 0
            
            cursor.close()
            conn.close()
            
            return {
                'total_rutinas': total_rutinas,
                'facil': por_nivel.get('facil', 0),
                'intermedio': por_nivel.get('intermedio', 0),
                'dificil': por_nivel.get('dificil', 0),
                'total_ejercicios': total_ejercicios
            }
        except sqlite3.Error as e:
            print(f"Error al obtener estadísticas de rutinas: {e}")
            return {
                'total_rutinas': 0,
                'facil': 0,
                'intermedio': 0,
                'dificil': 0,
                'total_ejercicios': 0
            }
