from Backend.Model.reserv_model import ReservaModel

class ReservasController:
    def __init__(self):
        self.modelo = ReservaModel()
    
    def crear_reserva(self, usuario_id, clase, fecha, hora, duracion=1):
        """Crea una nueva reserva"""
        return self.modelo.crear_reserva(usuario_id, clase, fecha, hora, duracion)
    
    def obtener_reservas_usuario(self, usuario_id):
        """Obtiene todas las reservas de un usuario"""
        return self.modelo.obtener_reservas_usuario(usuario_id)
    
    def marcar_asistencia(self, reserva_id):
        """Marca una reserva como asistida"""
        return self.modelo.marcar_asistencia(reserva_id)