from Backend.Model.reserv_model import ReservaModel
from Backend.Model.user_model import UserModel

class ReservasController:
    def __init__(self):
        self.modelo = ReservaModel()
        self.user_model = UserModel()
    
    def crear_reserva(self, usuario_id, maquina, fecha, hora, duracion=1):
        """Crea una nueva reserva"""
        return self.modelo.crear_reserva(usuario_id, maquina, fecha, hora, duracion)
    
    def obtener_reservas_usuario(self, usuario_id):
        """Obtiene todas las reservas de un usuario"""
        return self.modelo.obtener_reservas_usuario(usuario_id)
    
    def marcar_completada(self, reserva_id):
        """Marca una reserva como completada"""
        return self.modelo.marcar_completada(reserva_id)
    
    def verificar_y_procesar_reservas_vencidas(self):
        """
        Verifica reservas vencidas, las marca como completadas
        y actualiza el nivel de los usuarios correspondientes
        """
        # Obtener usuarios con reservas vencidas
        usuarios_afectados = self.modelo.procesar_reservas_vencidas()
        
        # Actualizar nivel para cada usuario
        for usuario_id in set(usuarios_afectados):  # set para evitar duplicados
            self.user_model.incrementar_reservas_completadas(usuario_id)
        
        return len(set(usuarios_afectados))  # Retorna cantidad de usuarios actualizados