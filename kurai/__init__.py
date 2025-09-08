"""
Kurai SDK - Cliente oficial para la API pública de Lexia
========================================================

Kurai es el SDK oficial para interactuar con todos los endpoints públicos de Lexia.
Proporciona una interfaz simple y pythónica para integrar Lexia en tus aplicaciones.

Ejemplo básico:
    import kurai
    
    # Configurar cliente
    client = kurai.Client(
        tenant_url="https://api.cloud.lexia.la",
        api_key="lx-xxxxxxxxxxxxxxxxxxxxx"
    )
    
    # Verificar conexión
    health = client.health_check()
    
    # Listar áreas
    areas = client.list_areas()
    
    # Subir documento
    result = client.upload_document("/path/to/file.pdf", area_id=1)
    
    # Trabajar con colas
    result = client.add_queue_item("mi_cola", {"task": "procesar"})

Copyright (c) 2024 Lexia SPA. Todos los derechos reservados.
Autor: Lexia Team
Versión: 1.0.0
"""

from .client import Client
from .exceptions import KuraiException

__version__ = "1.0.0"
__author__ = "Lexia Team"
__email__ = "dev@lexia.la"
__license__ = "Proprietary"
__copyright__ = "Copyright (c) 2024 Lexia SPA. Todos los derechos reservados."
__url__ = "https://github.com/lexia/kurai-sdk"

# Exportar las clases principales
__all__ = [
    "Client",
    "KuraiException",
    "__version__"
]

# Alias para compatibilidad
LexiaSDK = Client  # Para retrocompatibilidad
LexiaAPIException = KuraiException

# Funciones de conveniencia
def client(tenant_url=None, api_key=None, **kwargs):
    """
    Función de conveniencia para crear un cliente
    
    Args:
        tenant_url (str): URL del tenant de Lexia
        api_key (str): API Key para autenticación
        **kwargs: Argumentos adicionales para el cliente
    
    Returns:
        Client: Instancia del cliente de Kurai
    
    Ejemplo:
        import kurai
        client = kurai.client("https://api.cloud.lexia.la", "lx-xxxxx")
    """
    return Client(tenant_url=tenant_url, api_key=api_key, **kwargs)

def version():
    """Retorna la versión actual del SDK"""
    return __version__