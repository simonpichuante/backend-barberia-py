class AppError(Exception):
    def __init__(self, message="Error de aplicación", code=400):
        super().__init__(message)
        self.code = code

class NotFoundError(AppError):
    def __init__(self, message="Recurso no encontrado"):
        super().__init__(message, code=404)

class ForbiddenError(AppError):
    def __init__(self, message="No tienes permisos para esta operación"):
        super().__init__(message, code=403)
