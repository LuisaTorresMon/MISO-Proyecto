class ApiError(Exception):
    code = 422
    description = "Default message"

class TokenNoEnviado(ApiError):
    code = 403
    description = "No hay token en la solicitud"

class TokenVencido(ApiError):
    code = 401
    description = "El token no es válido o está vencido."

class CamposFaltantes(ApiError):
    code = 400
    description = "Los campos de la petición están incompletos o no cumplen el formato esperado"

class SizeInvalido(ApiError):
    code = 412
    description = "El campo Size es inválido"

class OfferInvalida(ApiError):
    code = 412
    description = "El campo Offer es inválido"

class ErrorServicio(ApiError):
    code = 500
    description = "Error al consumir el servicio."

class ErrorUUID(ApiError):
    code = 400
    description = "El id no es un valor string con formato uuid."

class PlanNoExiste(ApiError):
    code = 404
    description = "El plan con ese id no existe."