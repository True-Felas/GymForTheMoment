import mysql.connector
from mysql.connector import Error


class Database:
    # Configuración de la conexión
    HOST = 'localhost'
    USER = 'root'  # Tu usuario de MySQL
    PASSWORD = ''  # Tu contraseña (vacía por defecto en XAMPP)
    DATABASE = 'gimnasio_db'  # Este nombre se usará para la BD

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.conectar()
        self.crear_base_datos()
        self.crear_tablas()

    def conectar(self):
        """Establece la conexión con MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.HOST,
                user=self.USER,
                password=self.PASSWORD
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            raise

    def crear_base_datos(self):
        """Crea la base de datos si no existe"""
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.DATABASE}")
            self.cursor.execute(f"USE {self.DATABASE}")
            self.connection.commit()
        except Error as e:
            print(f"Error al crear base de datos: {e}")
            raise

    def crear_tablas(self):
        """Crea las tablas necesarias"""
        try:
            # Tabla de usuarios
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    nivel INT DEFAULT 1
                )
            ''')

            # Tabla de reservas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT NOT NULL,
                    clase VARCHAR(100) NOT NULL,
                    fecha DATE NOT NULL,
                    hora TIME NOT NULL,
                    duracion INT DEFAULT 1,
                    asistio BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                )
            ''')

            self.connection.commit()
        except Error as e:
            print(f"Error al crear tablas: {e}")
            raise

    def cerrar(self):
        """Cierra la conexión"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

    @staticmethod
    def get_connection():
        """Metodo estático para obtener una conexión a la base de datos"""
        try:
            connection = mysql.connector.connect(
                host=Database.HOST,
                user=Database.USER,
                password=Database.PASSWORD,
                database=Database.DATABASE
            )
            return connection
        except Error as e:
            print(f"Error al obtener conexión: {e}")
            raise
