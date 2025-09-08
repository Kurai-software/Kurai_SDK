"""
Excepciones personalizadas para Kurai SDK
=========================================

Copyright (c) 2024 Lexia SPA. Todos los derechos reservados.
"""


class KuraiException(Exception):
    """Excepción base para todos los errores de Kurai SDK"""
    
    def __init__(self, message, status_code=None, response_data=None, original_exception=None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        self.original_exception = original_exception
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
    
    def __repr__(self):
        return f"KuraiException(message='{self.message}', status_code={self.status_code})"


class KuraiConnectionError(KuraiException):
    """Error de conexión con la API de Lexia"""
    pass


class KuraiAuthenticationError(KuraiException):
    """Error de autenticación (API key inválida)"""
    pass


class KuraiNotFoundError(KuraiException):
    """Recurso no encontrado (404)"""
    pass


class KuraiValidationError(KuraiException):
    """Error de validación de parámetros (400)"""
    pass


class KuraiServerError(KuraiException):
    """Error interno del servidor (500+)"""
    pass


class KuraiConfigurationError(KuraiException):
    """Error de configuración del SDK"""
    pass


def create_exception_from_response(response, message=None):
    """
    Crea la excepción apropiada basada en el código de respuesta HTTP
    
    Args:
        response: Objeto Response de requests
        message: Mensaje personalizado (opcional)
    
    Returns:
        KuraiException: Excepción apropiada para el código de estado
    """
    try:
        response_data = response.json()
    except:
        response_data = {"error": response.text}
    
    error_message = message or response_data.get('error', f'HTTP {response.status_code}')
    
    # Mapear códigos de estado a excepciones específicas
    if response.status_code == 401:
        return KuraiAuthenticationError(
            message=error_message,
            status_code=response.status_code,
            response_data=response_data
        )
    elif response.status_code == 404:
        return KuraiNotFoundError(
            message=error_message,
            status_code=response.status_code,
            response_data=response_data
        )
    elif response.status_code == 400:
        return KuraiValidationError(
            message=error_message,
            status_code=response.status_code,
            response_data=response_data
        )
    elif response.status_code >= 500:
        return KuraiServerError(
            message=error_message,
            status_code=response.status_code,
            response_data=response_data
        )
    else:
        return KuraiException(
            message=error_message,
            status_code=response.status_code,
            response_data=response_data
        )