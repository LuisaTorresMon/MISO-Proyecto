class ApiError(Exception):
    def __init__(self, message):
        self.description = message or self.description
    code = 422
    description = "Default message"
    
class BadRequestError(ApiError):
    code = 400
    description = "En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado."

class CamposFaltantes(ApiError):
    code = 400
    description = ("Campos faltantes en la solicitud")
    
class ServerSystemException(ApiError):
    code = 500
    description = "Error en el sistema porfavor contacte con el administrador"