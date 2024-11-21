class ApiError(Exception):
    def __init__(self, message):
        self.description = message or self.description
    code = 422
    description = "Default message"

class IAPredictionException(ApiError):
    code = 500
    description = "Error en la predicción"