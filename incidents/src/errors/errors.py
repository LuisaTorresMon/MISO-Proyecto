class ApiError(Exception):
    def __init__(self, message):
        self.description = message or self.description
    code = 422
    description = "Default message"
    
class BadRequestError(ApiError):
    code = 400
    description = "En el caso que alguno de los campos no esté presente en la solicitud, o no tengan el formato esperado."

class RequiredFields(ApiError):
    code = 400
    description = ("Campos faltantes en la solicitud")
    
class ServerSystemException(ApiError):
    code = 500
    description = "Error en el sistema porfavor contacte con el administrador"
    
class InvalidToken(ApiError):
    code = 401
    description = "El token no es válido o está vencido."
    
class ErrorService(ApiError):
    code = 500
    description = "Error a la hora de consumir el servicio."
    
class TokenEmpty(ApiError):
    code = 403
    description = "No hay token en la solicitud"