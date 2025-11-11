import sqlite3
import os


class Database:
    # Configuración de la conexión SQLite
    DB_PATH = os.path.join(os.path.dirname(__file__), 'gimnasio.db')

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.conectar()
        self.crear_tablas()

    def conectar(self):
        """Establece la conexión con SQLite"""
        try:
            self.connection = sqlite3.connect(self.DB_PATH)
            self.cursor = self.connection.cursor()
            # Habilitar foreign keys en SQLite
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            print(f"Error al conectar a SQLite: {e}")
            raise

    def crear_tablas(self):
        """Crea las tablas necesarias"""
        try:
            # Tabla de usuarios
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nivel INTEGER DEFAULT 1,
                    reservas_completadas INTEGER DEFAULT 0
                )
            ''')

            # Tabla de reservas (ahora para máquinas)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    maquina TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    duracion INTEGER DEFAULT 1,
                    completada INTEGER DEFAULT 0,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                )
            ''')

            # Tabla de pagos mensuales
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    mes INTEGER NOT NULL,
                    anio INTEGER NOT NULL,
                    monto REAL NOT NULL,
                    pagado INTEGER DEFAULT 0,
                    fecha_pago TEXT,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                    UNIQUE(usuario_id, mes, anio)
                )
            ''')

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")
            raise

    def cerrar(self):
        """Cierra la conexión"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    @staticmethod
    def get_connection():
        """Método estático para obtener una conexión a la base de datos"""
        try:
            connection = sqlite3.connect(Database.DB_PATH)
            # Habilitar foreign keys
            connection.execute("PRAGMA foreign_keys = ON")
            return connection
        except sqlite3.Error as e:
            print(f"Error al obtener conexión: {e}")
            raise
