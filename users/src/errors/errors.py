class ApiError(Exception):
    code = 422
    description = "Default message"

class TokenNoEnviado(ApiError):
    code = 403
    description = "No hay token en la solicitud"

class TokenVencido(ApiError):
    code = 401
    description = "El token no es válido o está vencido."

class BadRequestException(ApiError):
    code = 400
    description = "Los campos de la petición están incompletos o no cumplen el formato esperado"

class UserAlreadyExistException(ApiError):
    code = 409
    description = "Usuario ya existe en el sistema"

class IncorrectUserOrPasswordException(ApiError):
    code = 401
    description = "Usuario o contraseña incorrectos"