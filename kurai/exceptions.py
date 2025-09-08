"""
Excepciones personalizadas para Kurai SDK
==========================================

Este módulo define todas las excepciones específicas que puede lanzar el SDK de Kurai.
Permite un manejo de errores más granular y específico para diferentes tipos de fallos.

Copyright (c) 2024 Lexia SPA. Todos los derechos reservados.
"""

import requests
from typing import Optional, Dict, Any


class KuraiException(Exception):
    """
    Excepción base para todos los errores del SDK de Kurai.
    
    Todas las demás excepciones específicas heredan de esta clase.
    """
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        """
        Inicializar excepción base.
        
        Args:
            message: Mensaje descriptivo del error
            status_code: Código de estado HTTP si aplica
            response_data: Datos de respuesta del servidor si están disponibles
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
    
    def __str__(self):
        """Representación string de la excepción."""
        if self.status_code:
            return f"Kurai Error [{self.status_code}]: {self.message}"
        return f"Kurai Error: {self.message}"
    
    def __repr__(self):
        """Representación técnica de la excepción."""
        return f"KuraiException(message='{self.message}', status_code={self.status_code})"


class KuraiAuthenticationError(KuraiException):
    """Error de autenticación con la API de Lexia."""
    
    def __init__(self, message: str = "Error de autenticación con la API", **kwargs):
        super().__init__(message, **kwargs)


class KuraiValidationError(KuraiException):
    """Error de validación de datos."""
    
    def __init__(self, message: str = "Error de validación de datos", **kwargs):
        super().__init__(message, **kwargs)


class KuraiConnectionError(KuraiException):
    """Error de conexión con la API."""
    
    def __init__(self, message: str = "Error de conexión con la API", **kwargs):
        super().__init__(message, **kwargs)


class KuraiServerError(KuraiException):
    """Error interno del servidor de Lexia."""
    
    def __init__(self, message: str = "Error interno del servidor", **kwargs):
        super().__init__(message, **kwargs)


class KuraiNotFoundError(KuraiException):
    """Recurso no encontrado."""
    
    def __init__(self, message: str = "Recurso no encontrado", **kwargs):
        super().__init__(message, **kwargs)


class KuraiRateLimitError(KuraiException):
    """Límite de velocidad excedido."""
    
    def __init__(self, message: str = "Límite de velocidad excedido", retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class KuraiFileError(KuraiException):
    """Error relacionado con archivos."""
    
    def __init__(self, message: str = "Error de archivo", **kwargs):
        super().__init__(message, **kwargs)


class KuraiConfigurationError(KuraiException):
    """Error de configuración del SDK."""
    
    def __init__(self, message: str = "Error de configuración", **kwargs):
        super().__init__(message, **kwargs)


def create_exception_from_response(response: requests.Response) -> KuraiException:
    """
    Crear la excepción apropiada basada en la respuesta HTTP.
    """
    try:
        response_data = response.json()
        error_message = response_data.get('error', 'Error desconocido')
        detail = response_data.get('detail', '')
        
        if detail:
            error_message += f": {detail}"
            
    except (ValueError, KeyError):
        error_message = f"Error HTTP {response.status_code}"
        response_data = {}
    
    status_code = response.status_code
    
    if status_code == 401:
        return KuraiAuthenticationError(
            message=error_message,
            status_code=status_code,
            response_data=response_data
        )
    elif status_code == 400:
        return KuraiValidationError(
            message=error_message,
            status_code=status_code,
            response_data=response_data
        )
    elif status_code == 404:
        return KuraiNotFoundError(
            message=error_message,
            status_code=status_code,
            response_data=response_data
        )
    elif status_code == 429:
        retry_after = None
        if 'Retry-After' in response.headers:
            try:
                retry_after = int(response.headers['Retry-After'])
            except ValueError:
                pass
                
        return KuraiRateLimitError(
            message=error_message,
            status_code=status_code,
            response_data=response_data,
            retry_after=retry_after
        )
    elif 500 <= status_code < 600:
        return KuraiServerError(
            message=error_message,
            status_code=status_code,
            response_data=response_data
        )
    else:
        return KuraiException(
            message=error_message,
            status_code=status_code,
            response_data=response_data
        )


# Exportar todas las excepciones
__all__ = [
    'KuraiException',
    'KuraiAuthenticationError', 
    'KuraiValidationError',
    'KuraiConnectionError',
    'KuraiServerError',
    'KuraiNotFoundError',
    'KuraiRateLimitError',
    'KuraiFileError',
    'KuraiConfigurationError',
    'create_exception_from_response'
]