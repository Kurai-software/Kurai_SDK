"""
Cliente principal de Kurai SDK
==============================

Cliente para interactuar con todos los endpoints públicos de la API de Lexia.

Copyright (c) 2024 Lexia SPA. Todos los derechos reservados.
"""

import requests
import json
import os
from typing import Dict, List, Optional, Union
from .exceptions import (
    KuraiException, 
    KuraiConnectionError, 
    KuraiConfigurationError,
    create_exception_from_response
)


class Client:
    """
    Cliente principal de Kurai SDK para la API pública de Lexia
    
    Ejemplo:
        import kurai
        
        client = kurai.Client(
            tenant_url="https://api.cloud.lexia.la",
            api_key="lx-xxxxxxxxxxxxxxxxxxxxx"
        )
        
        # Verificar conexión
        health = client.health_check()
        
        # Subir documento
        result = client.upload_document("/path/to/file.pdf", area_id=1)
    """
    
    def __init__(self, tenant_url: str = None, api_key: str = None, timeout: int = 30):
        """
        Inicializar el cliente de Kurai
        
        Args:
            tenant_url (str): URL base del tenant (ej: https://api.cloud.lexia.la)
            api_key (str): Clave de API válida
            timeout (int): Timeout para las requests en segundos
            
        Raises:
            KuraiConfigurationError: Si faltan parámetros requeridos
        """
        # Configurar desde parámetros o variables de entorno
        self.tenant_url = tenant_url or os.getenv('LEXIA_TENANT_URL')
        self.api_key = api_key or os.getenv('LEXIA_API_KEY')
        
        if not self.tenant_url:
            raise KuraiConfigurationError(
                "Se requiere tenant_url. Configúralo como parámetro o variable de entorno LEXIA_TENANT_URL"
            )
        
        if not self.api_key:
            raise KuraiConfigurationError(
                "Se requiere api_key. Configúralo como parámetro o variable de entorno LEXIA_API_KEY"
            )
        
        # Limpiar URL
        self.tenant_url = self.tenant_url.rstrip('/')
        self.timeout = timeout
        
        # Configurar session
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': f'Kurai-SDK/1.0.0'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Realizar una request HTTP
        
        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE, PATCH)
            endpoint (str): Endpoint de la API
            **kwargs: Argumentos adicionales para requests
            
        Returns:
            requests.Response: Respuesta de la API
            
        Raises:
            KuraiException: Error en la API o conexión
        """
        url = f"{self.tenant_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            if not response.ok:
                raise create_exception_from_response(response)
            
            return response
            
        except requests.exceptions.ConnectionError as e:
            raise KuraiConnectionError(f"Error de conexión: {str(e)}")
        except requests.exceptions.Timeout as e:
            raise KuraiConnectionError(f"Timeout de conexión: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise KuraiConnectionError(f"Error de request: {str(e)}")
    
    def _get(self, endpoint: str, params: dict = None) -> dict:
        """GET request helper"""
        response = self._make_request('GET', endpoint, params=params)
        return response.json()
    
    def _post(self, endpoint: str, data: dict = None, files: dict = None) -> dict:
        """POST request helper"""
        if files:
            # Para uploads, no establecer Content-Type
            original_headers = self.session.headers.copy()
            if 'Content-Type' in self.session.headers:
                del self.session.headers['Content-Type']
            
            response = self._make_request('POST', endpoint, data=data, files=files)
            self.session.headers = original_headers
        else:
            response = self._make_request('POST', endpoint, json=data)
        
        return response.json()
    
    def _put(self, endpoint: str, data: dict = None) -> dict:
        """PUT request helper"""
        response = self._make_request('PUT', endpoint, json=data)
        return response.json()
    
    def _delete(self, endpoint: str, data: dict = None) -> dict:
        """DELETE request helper"""
        response = self._make_request('DELETE', endpoint, json=data)
        return response.json()
    
    def _patch(self, endpoint: str, data: dict = None) -> dict:
        """PATCH request helper"""
        # Para PATCH requests, enviar como form-data en lugar de JSON
        if data:
            # Remover temporalmente Content-Type para que requests use form-data
            original_headers = self.session.headers.copy()
            if 'Content-Type' in self.session.headers:
                del self.session.headers['Content-Type']
            
            response = self._make_request('PATCH', endpoint, data=data)
            self.session.headers = original_headers
        else:
            # Si no hay datos, enviar request vacío
            response = self._make_request('PATCH', endpoint, data={})
        
        return response.json()
    
    # ==============================================
    # UTILIDADES
    # ==============================================
    
    def health_check(self) -> dict:
        """
        Verificar el estado de la API
        
        Returns:
            dict: Estado de la API
            
        Ejemplo:
            health = client.health_check()
            if health['status'] == 'ok':
                print("API funcionando")
        """
        try:
            # Intentar obtener áreas como health check
            result = self.list_areas()
            return {"status": "ok", "api_accessible": True}
        except Exception as e:
            return {"status": "error", "error": str(e), "api_accessible": False}
    
    # ==============================================
    # ÁREAS API
    # ==============================================
    
    def list_areas(self) -> dict:
        """
        Listar todas las áreas disponibles
        
        Returns:
            dict: Lista de áreas
            
        Ejemplo:
            areas = client.list_areas()
            for area in areas['areas']:
                print(f"{area['nombre']} (ID: {area['id']})")
        """
        return self._get('/public/api/areas')
    
    # ==============================================
    # DOCUMENTOS API
    # ==============================================
    
    def upload_document(self, file_path: str, area_id: int, description: str = "") -> dict:
        """
        Subir un documento
        
        Args:
            file_path (str): Ruta al archivo
            area_id (int): ID del área
            description (str): Descripción del documento
            
        Returns:
            dict: Información del documento subido
            
        Ejemplo:
            result = client.upload_document(
                file_path="/path/to/invoice.pdf",
                area_id=1,
                description="Factura enero 2024"
            )
        """
        if not os.path.exists(file_path):
            raise KuraiException(f"Archivo no encontrado: {file_path}")
        
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/octet-stream')}
            data = {
                'area_id': area_id,
                'description': description
            }
            
            return self._post('/public/api/upload', data=data, files=files)
    
    def upload_and_process_document(self, file_path: str, area_id: int, description: str = "") -> dict:
        """
        Subir y procesar un documento automáticamente
        
        Args:
            file_path (str): Ruta al archivo
            area_id (int): ID del área
            description (str): Descripción del documento
            
        Returns:
            dict: Información del documento subido y procesado
        """
        if not os.path.exists(file_path):
            raise KuraiException(f"Archivo no encontrado: {file_path}")
        
        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/octet-stream')}
            data = {
                'area_id': area_id,
                'description': description
            }
            
            return self._post('/public/api/upload-and-process', data=data, files=files)
    
    def get_document_extracted_data(self, document_id: int) -> dict:
        """
        Obtener JSON extraído de un documento específico
        
        Args:
            document_id (int): ID del documento
            
        Returns:
            dict: Datos extraídos del documento
        """
        return self._get(f'/public/api/documents/{document_id}/extracted-data')
    
    def get_documents_extracted_data_batch(self, document_ids: List[int]) -> dict:
        """
        Obtener JSON extraído de múltiples documentos
        
        Args:
            document_ids (List[int]): Lista de IDs de documentos
            
        Returns:
            dict: Datos extraídos de los documentos
        """
        return self._post('/public/api/documents/extracted-data/batch', 
                         data={'document_ids': document_ids})
    
    def list_processed_documents(self, page: int = 1, per_page: int = 50, 
                                area_id: int = None, status: str = None) -> dict:
        """
        Listar documentos procesados con paginación y filtros
        
        Args:
            page (int): Número de página
            per_page (int): Documentos por página
            area_id (int): Filtrar por área
            status (str): Filtrar por estado
            
        Returns:
            dict: Lista de documentos procesados
        """
        params = {'page': page, 'per_page': per_page}
        if area_id:
            params['area_id'] = area_id
        if status:
            params['status'] = status
            
        return self._get('/public/api/documents/processed', params=params)
    
    def get_document_url(self, document_id: int) -> dict:
        """
        Obtener URL de un documento por ID
        
        Args:
            document_id (int): ID del documento
            
        Returns:
            dict: URL del documento
        """
        return self._get(f'/public/api/documents/{document_id}/url')
    
    def bulk_delete_documents(self, document_ids: List[int]) -> dict:
        """
        Eliminar múltiples documentos
        
        Args:
            document_ids (List[int]): Lista de IDs de documentos a eliminar
            
        Returns:
            dict: Resultado de la operación
        """
        return self._delete('/public/api/documents/bulk', 
                           data={'document_ids': document_ids})
    
    # ==============================================
    # COLAS API
    # ==============================================
    
    def add_queue_item(self, queue_name: str, data: dict, priority: int = 0) -> dict:
        """
        Agregar un elemento a una cola
        
        Args:
            queue_name (str): Nombre o ID de la cola
            data (dict): Datos del elemento
            priority (int): Prioridad (0=Low, 1=Medium, 2=High)
            
        Returns:
            dict: Información del elemento agregado
        """
        # Convertir prioridad numérica a string
        priority_map = {0: "Low", 1: "Medium", 2: "High"}
        priority_str = priority_map.get(priority, "Medium")
        
        return self._post('/public/api/queues/add-item', data={
            'queue': queue_name,
            'data': data,
            'priority': priority_str
        })
    
    def get_next_queue_item(self, queue_name: str, status: str = "New", 
                           priority_order: bool = True, mark_as_processing: bool = False) -> dict:
        """
        Obtener el siguiente elemento de una cola
        
        Args:
            queue_name (str): Nombre o ID de la cola
            status (str): Estado del item ("New", "In Progress", "Successful", "Failed")
            priority_order (bool): Si debe respetar prioridad
            mark_as_processing (bool): Si debe marcar como "In Progress" automáticamente
            
        Returns:
            dict: Siguiente elemento de la cola
        """
        params = {
            'queue': queue_name,
            'status': status,
            'priority_order': str(priority_order).lower(),
            'mark_as_processing': str(mark_as_processing).lower()
        }
        return self._get('/public/api/queues/next-item', params=params)
    
    def update_queue_item(self, item_id: str, data: dict = None, status: str = None, 
                         merge_mode: str = "update", etapa: str = None) -> dict:
        """
        Actualizar un elemento de cola
        
        Args:
            item_id (str): ID del elemento (UUID)
            data (dict): Nuevos datos del elemento
            status (str): Nuevo estado del elemento
            merge_mode (str): "update" o "replace"
            etapa (str): Nueva etapa
            
        Returns:
            dict: Elemento actualizado
        """
        update_data = {
            'item_id': item_id,
            'merge_mode': merge_mode
        }
        
        if data:
            update_data['data'] = data
        if status:
            update_data['status'] = status
        if etapa:
            update_data['etapa'] = etapa
            
        return self._post('/public/api/queues/items/update-data', data=update_data)
    
    def bulk_delete_queue_items(self, item_ids: List[str]) -> dict:
        """
        Eliminar múltiples elementos de cola
        
        Args:
            item_ids (List[str]): Lista de IDs de elementos a eliminar (UUIDs)
            
        Returns:
            dict: Resultado de la operación
        """
        return self._delete('/public/api/queues/items/bulk', 
                           data={'item_ids': item_ids})
    
    def get_queue_analytics(self, period: str = '24h') -> dict:
        """
        Obtener analíticas de colas
        
        Args:
            period (str): Período de análisis ('24h', '7d', '30d')
            
        Returns:
            dict: Analíticas de las colas
        """
        return self._get('/public/api/queues/analytics', params={'period': period})
    
    def finish_queue_item(self, item_id: str, output: dict = None, 
                         progress: int = 100, etapa: str = None) -> dict:
        """
        Finalizar un elemento de cola marcándolo como "Successful" automáticamente
        
        Este método es una forma conveniente de marcar un elemento como completado exitosamente.
        Automáticamente establece el status como "Successful", registra el timestamp de finalización
        y combina los datos de salida con la información existente.
        
        Args:
            item_id (str): ID del elemento de cola (UUID)
            output (dict): Datos de salida del procesamiento (opcional)
            progress (int): Progreso del elemento (por defecto 100%)
            etapa (str): Nueva etapa descriptiva (opcional, máximo 255 caracteres)
            
        Returns:
            dict: Información del elemento finalizado
            
        Raises:
            KuraiException: Si hay un error en la API
            
        Ejemplo:
            # Finalizar con resultados
            result = client.finish_queue_item(
                item_id="ca9cf1c9-9d9b-4b24-8547-63d1c5265fbf",
                output={
                    "resultado": "Documento procesado exitosamente",
                    "datos_extraidos": {"total": "$1,500.00", "fecha": "2024-01-15"},
                    "tiempo_procesamiento": "2.3 segundos",
                    "precision": "99.2%"
                },
                etapa="Procesamiento completado"
            )
            
            # Finalizar simple sin datos de salida
            result = client.finish_queue_item(
                item_id="550e8400-e29b-41d4-a716-446655440000"
            )
            
            # Finalizar con progreso personalizado
            result = client.finish_queue_item(
                item_id="abc12345-def6-7890-abcd-123456789012",
                output={"status": "Procesado parcialmente"},
                progress=95,
                etapa="Completado con advertencias"
            )
        """
        # Validar que item_id no esté vacío
        if not item_id or not item_id.strip():
            raise KuraiException("item_id es requerido y no puede estar vacío")
        
        # Validar progreso
        if not isinstance(progress, int) or progress < 0 or progress > 100:
            raise KuraiException("progress debe ser un entero entre 0 y 100")
        
        # Validar longitud de etapa
        if etapa and len(etapa) > 255:
            raise KuraiException("etapa no puede tener más de 255 caracteres")
        
        # Preparar datos para el request
        finish_data = {
            "progress": progress
        }
        
        if output:
            finish_data["output"] = json.dumps(output)  # Convertir dict a JSON string para form-data
        
        if etapa:
            finish_data["etapa"] = etapa
        
        # Realizar request PATCH
        return self._patch(f'/public/api/queues/items/{item_id}/finish', data=finish_data)
    
    # ==============================================
    # GRIDS API
    # ==============================================
    
    def get_grid_data(self, grid_id: int, page: int = 1, per_page: int = 50, 
                     filters: dict = None) -> dict:
        """
        Obtener datos de un grid
        
        Args:
            grid_id (int): ID del grid
            page (int): Número de página
            per_page (int): Elementos por página
            filters (dict): Filtros a aplicar
            
        Returns:
            dict: Datos del grid
        """
        params = {'page': page, 'per_page': per_page}
        if filters:
            params.update(filters)
            
        return self._get(f'/api/public/grids/{grid_id}/data', params=params)
    
    def get_grid_info(self, grid_id: int) -> dict:
        """
        Obtener información de un grid
        
        Args:
            grid_id (int): ID del grid
            
        Returns:
            dict: Información del grid
        """
        return self._get(f'/api/public/grids/{grid_id}/info')
    
    # ==============================================
    # CORREOS API
    # ==============================================
    
    def get_email_by_id(self, email_id: str) -> dict:
        """
        Obtener un correo por su ID
        
        Args:
            email_id (str): ID del correo
            
        Returns:
            dict: Detalles completos del correo
        """
        return self._get('/public/api/correo', params={'email_id': email_id})
    
    def reply_to_email(self, email_id: str, mensaje: str, tipo_respuesta: str = "texto", 
                      asunto_personalizado: str = None, archivos: List[tuple] = None) -> dict:
        """
        Responder a un correo electrónico
        
        Args:
            email_id (str): ID del correo original
            mensaje (str): Contenido de la respuesta
            tipo_respuesta (str): "texto" o "html"
            asunto_personalizado (str): Asunto personalizado (opcional)
            archivos (List[tuple]): Lista de tuplas (nombre_archivo, contenido_bytes) para adjuntos
            
        Returns:
            dict: Resultado del envío
        """
        if archivos:
            # Usar multipart/form-data para adjuntos
            files = {}
            data = {
                'email_id': email_id,
                'mensaje': mensaje,
                'tipo_respuesta': tipo_respuesta
            }
            
            if asunto_personalizado:
                data['asunto_personalizado'] = asunto_personalizado
            
            # Agregar archivos
            for i, (filename, file_content) in enumerate(archivos):
                files[f'archivos'] = (filename, file_content, 'application/octet-stream')
            
            return self._post('/public/api/correo/responder', data=data, files=files)
        else:
            # Usar JSON para respuestas simples
            data = {
                'email_id': email_id,
                'mensaje': mensaje,
                'tipo_respuesta': tipo_respuesta
            }
            
            if asunto_personalizado:
                data['asunto_personalizado'] = asunto_personalizado
            
            return self._post('/public/api/correo/responder', data=data)

    def send_email(self, to, subject, body, body_type="html", cc=None, bcc=None, 
        reply_to=None, body_text=None, archivos=None) -> dict:
        """
        Enviar un correo electrónico nuevo
        
        Args:
            to (str|list): Destinatario(s) del correo
            subject (str): Asunto del correo
            body (str): Cuerpo del mensaje
            body_type (str): "html" o "texto" (por defecto "html")
            cc (str|list): Destinatarios CC (opcional)
            bcc (str|list): Destinatarios BCC (opcional)
            reply_to (str): Dirección de respuesta (opcional)
            body_text (str): Versión texto plano del mensaje (opcional)
            archivos (List[tuple]): Lista de tuplas (nombre_archivo, contenido_bytes) para adjuntos
            
        Returns:
            dict: Resultado del envío
            
        Ejemplo:
            # Envío simple
            result = client.send_email(
                to="destinatario@ejemplo.com",
                subject="Hola desde Kurai",
                body="<h1>¡Funciona!</h1><p>SDK funcionando correctamente.</p>"
            )
            
            # Con múltiples destinatarios y adjuntos
            with open("archivo.pdf", "rb") as f:
                archivo_data = f.read()
                
            result = client.send_email(
                to=["user1@test.com", "user2@test.com"],
                cc=["supervisor@test.com"],
                subject="Reporte mensual",
                body="<p>Adjunto el reporte del mes.</p>",
                archivos=[("reporte.pdf", archivo_data)]
            )
        """
        # Normalizar destinatarios
        if isinstance(to, str):
            to = [to]
        
        email_data = {
            'to': to,
            'subject': subject,
            'body': body,
            'body_type': body_type
        }
        
        # Agregar campos opcionales
        if cc:
            if isinstance(cc, str):
                cc = [cc]
            email_data['cc'] = cc
        
        if bcc:
            if isinstance(bcc, str):
                bcc = [bcc]
            email_data['bcc'] = bcc
        
        if reply_to:
            email_data['reply_to'] = reply_to
        
        if body_text:
            email_data['body_text'] = body_text
        
        # Si hay archivos, usar multipart/form-data
        if archivos:
            # Convertir listas a strings para form-data
            form_data = email_data.copy()
            if isinstance(form_data.get('to'), list):
                form_data['to'] = ', '.join(form_data['to'])
            if isinstance(form_data.get('cc'), list):
                form_data['cc'] = ', '.join(form_data['cc'])
            if isinstance(form_data.get('bcc'), list):
                form_data['bcc'] = ', '.join(form_data['bcc'])
            
            files = {}
            for i, (filename, file_content) in enumerate(archivos):
                files['archivos'] = (filename, file_content, 'application/octet-stream')
            
            return self._post('/public/api/correo/enviar', data=form_data, files=files)
        else:
            # Usar JSON para envío simple
            return self._post('/public/api/correo/enviar', data=email_data)

    def send_simple_email(self, to, subject, body, body_type="html") -> dict:
        """
        Método de conveniencia para enviar un correo simple sin adjuntos
        
        Args:
            to (str): Destinatario del correo
            subject (str): Asunto del correo
            body (str): Cuerpo del mensaje
            body_type (str): "html" o "texto" (por defecto "html")
            
        Returns:
            dict: Resultado del envío
            
        Ejemplo:
            result = client.send_simple_email(
                to="usuario@ejemplo.com",
                subject="Notificación importante",
                body="<p>Tu documento ha sido procesado exitosamente.</p>"
            )
        """
        return self.send_email(to=to, subject=subject, body=body, body_type=body_type)

    def send_notification_email(self, to, template_type, template_data=None) -> dict:
        """
        Enviar email usando plantillas predefinidas del sistema
        
        Args:
            to (str): Destinatario del correo
            template_type (str): Tipo de plantilla ("document_processed", "queue_completed", etc.)
            template_data (dict): Datos para rellenar la plantilla
            
        Returns:
            dict: Resultado del envío
            
        Ejemplo:
            result = client.send_notification_email(
                to="usuario@ejemplo.com",
                template_type="document_processed",
                template_data={
                    "document_name": "factura_enero.pdf",
                    "processing_time": "2.3 segundos",
                    "extracted_data": {"total": "$1,500.00"}
                }
            )
        """
        email_data = {
            'to': [to] if isinstance(to, str) else to,
            'template_type': template_type,
            'template_data': template_data or {}
        }
        
        return self._post('/public/api/correo/notification', data=email_data)