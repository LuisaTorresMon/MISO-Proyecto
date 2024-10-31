class ApiError(Exception):
    code = 500
    description = "Ha ocurrido un error en el servidor"

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
    
class RequiredFields(ApiError):
    code = 400
    description = "Campos faltantes en la solicitud"
    
class ServerSystemException(ApiError):
    code = 500
    description = "Error en el sistema porfavor contacte con el administrador"

class EmailInvalido(ApiError):
    code = 400
    description = "El formato del email no es válido"

class TelefonoNoNumerico(ApiError):
    code = 400
    description = "El campo de teléfono debe contener solo números"

class PassNoCoincide(ApiError):
    code = 400
    description = "Las contraseñas no coinciden"
    
class ResourceNotFound(ApiError):
    code = 404
    description = "El recurso no ha sido encontrado"

class PassNoValido(ApiError):
    code = 400
    description = "La contraseña debe tener al menos 8 caracteres, incluyendo una letra mayúscula, una letra minúscula y un número" 
    
