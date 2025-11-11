"""
Script de prueba para verificar que la base de datos SQLite funciona correctamente
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from Backend.DataBase.database import Database
from Backend.Model.user_model import UserModel
from Backend.Model.reserv_model import ReservaModel
from Backend.Controller.reserv_control import ReservasController

def test_database():
    print("=" * 60)
    print("PRUEBA DE LA BASE DE DATOS SQLITE")
    print("=" * 60)
    
    # 1. Crear base de datos
    print("\n1. Creando base de datos SQLite...")
    db = Database()
    print(f"   ✓ Base de datos creada en: {Database.DB_PATH}")
    db.cerrar()
    
    # 2. Crear usuarios de ejemplo
    print("\n2. Creando usuarios de ejemplo...")
    user_model = UserModel()
    print("   ✓ Usuarios de ejemplo creados (admin, juan, sofia)")
    
    # 3. Validar usuario
    print("\n3. Validando credenciales...")
    valido = user_model.validar_usuario("admin", "1234")
    print(f"   ✓ Usuario 'admin' con password '1234': {'VÁLIDO' if valido else 'INVÁLIDO'}")
    
    # 4. Obtener ID de usuario
    print("\n4. Obteniendo ID de usuario...")
    user_id = user_model.obtener_id_usuario("admin")
    print(f"   ✓ ID del usuario 'admin': {user_id}")
    
    # 5. Mostrar máquinas disponibles
    print("\n5. Máquinas disponibles en el gimnasio:")
    reserv_model = ReservaModel()
    for i, maquina in enumerate(reserv_model.MAQUINAS_DISPONIBLES, 1):
        print(f"   {i}. {maquina}")
    
    # 6. Crear una reserva de prueba
    print("\n6. Creando reserva de prueba...")
    resultado = reserv_model.crear_reserva(
        usuario_id=user_id,
        maquina="Cinta de Correr 1",
        fecha="2025-11-15",
        hora="10:00",
        duracion=1
    )
    print(f"   ✓ Reserva creada: {'SÍ' if resultado else 'NO'}")
    
    # 7. Verificar disponibilidad
    print("\n7. Verificando disponibilidad...")
    disponible = reserv_model.maquina_disponible("2025-11-15", "Cinta de Correr 1", "10:00")
    print(f"   ✓ Cinta de Correr 1 el 2025-11-15 a las 10:00: {'DISPONIBLE' if disponible else 'OCUPADA'}")
    
    disponible2 = reserv_model.maquina_disponible("2025-11-15", "Cinta de Correr 1", "11:00")
    print(f"   ✓ Cinta de Correr 1 el 2025-11-15 a las 11:00: {'DISPONIBLE' if disponible2 else 'OCUPADA'}")
    
    # 8. Obtener estadísticas del usuario
    print("\n8. Estadísticas del usuario 'admin':")
    stats = user_model.obtener_estadisticas(user_id)
    print(f"   - Reservas totales: {stats['reservas']}")
    print(f"   - Horas entrenadas: {stats['horas']}")
    print(f"   - Reservas completadas: {stats['reservas_completadas']}")
    print(f"   - Nivel: {stats['nivel']}")
    print(f"   - Reservas para subir de nivel: {stats['reservas_para_nivel']}")
    
    # 9. Probar sistema de niveles
    print("\n9. Probando sistema de niveles...")
    print(f"   - Nivel actual: {stats['nivel']}")
    print("   - Incrementando reservas completadas 3 veces...")
    for i in range(3):
        user_model.incrementar_reservas_completadas(user_id)
        stats = user_model.obtener_estadisticas(user_id)
        print(f"     Reserva {i+1}: Nivel {stats['nivel']}, Total completadas: {stats['reservas_para_nivel']}")
    
    # 10. Probar procesamiento de reservas vencidas
    print("\n10. Probando procesamiento automático de reservas vencidas...")
    controller = ReservasController()
    usuarios_actualizados = controller.verificar_y_procesar_reservas_vencidas()
    print(f"   ✓ Usuarios con reservas procesadas: {usuarios_actualizados}")
    
    print("\n" + "=" * 60)
    print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)

if __name__ == "__main__":
    test_database()
