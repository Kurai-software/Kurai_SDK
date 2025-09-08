# 🚀 Kurai SDK

**Cliente oficial para la API pública de Lexia**

[![PyPI version](https://badge.fury.io/py/kurai-sdk.svg)](https://badge.fury.io/py/kurai-sdk)
[![Python versions](https://img.shields.io/pypi/pyversions/kurai-sdk.svg)](https://pypi.org/project/kurai-sdk/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)

Kurai es el SDK oficial en Python para interactuar con todos los endpoints públicos de la API de Lexia. Proporciona una interfaz simple y pythónica para integrar las funcionalidades de automatización y procesamiento de documentos de Lexia en tus aplicaciones.

## ✨ Características

- 🔐 **Autenticación automática** con API Key
- 📄 **Gestión completa de documentos** (subida, procesamiento, extracción)
- 🚀 **Sistema de colas** para automatización
- 📊 **Acceso a grids y datos**
- 📧 **Manejo de correos electrónicos**
- 🛡️ **Manejo robusto de errores**
- 💻 **CLI incluido**
- 📚 **Documentación completa**
- 🐍 **Compatible con Python 3.7+**

## 📦 Instalación

```bash
pip install kurai-sdk
```

## ⚡ Inicio Rápido

```python
import kurai

# Configurar cliente
client = kurai.Client(
    tenant_url="https://api.cloud.lexia.la",
    api_key="lx-xxxxxxxxxxxxxxxxxxxxx"
)

# Verificar conexión
health = client.health_check()
print(f"Estado: {health['status']}")

# Listar áreas disponibles
areas = client.list_areas()
for area in areas['areas']:
    print(f"Área: {area['nombre']} (ID: {area['id']})")

# Subir documento
result = client.upload_document(
    file_path="/path/to/document.pdf",
    area_id=1,
    description="Mi documento importante"
)

# Trabajar con colas
result = client.add_queue_item(
    queue_name="procesamiento",
    data={"task": "extraer_datos", "priority": "high"},
    priority=2
)
```

## 🔧 Configuración

### Opción 1: Parámetros directos
```python
import kurai

client = kurai.Client(
    tenant_url="https://api.cloud.lexia.la",
    api_key="lx-xxxxxxxxxxxxxxxxxxxxx"
)
```

### Opción 2: Variables de entorno
```bash
export LEXIA_TENANT_URL="https://api.cloud.lexia.la"
export LEXIA_API_KEY="lx-xxxxxxxxxxxxxxxxxxxxx"
```

```python
import kurai
client = kurai.Client()  # Usa variables de entorno automáticamente
```

### Opción 3: Función de conveniencia
```python
import kurai
client = kurai.client("https://api.cloud.lexia.la", "lx-xxxxx")
```

## 📚 Funcionalidades Principales

### 📄 Gestión de Documentos

```python
# Subir documento simple
result = client.upload_document("/path/to/file.pdf", area_id=1)

# Subir y procesar automáticamente
result = client.upload_and_process_document(
    "/path/to/invoice.pdf", 
    area_id=1,
    description="Factura para procesar"
)

# Obtener datos extraídos
data = client.get_document_extracted_data(document_id=123)

# Listar documentos procesados
docs = client.list_processed_documents(page=1, per_page=50)

# Eliminar múltiples documentos
result = client.bulk_delete_documents([10, 11, 12])
```

### 🚀 Sistema de Colas

```python
# Agregar elemento a cola
result = client.add_queue_item(
    queue_name="mi_cola",
    data={"document_id": 123, "action": "extract_data"},
    priority=2  # 0=Low, 1=Medium, 2=High
)

# Obtener siguiente elemento para procesar
next_item = client.get_next_queue_item(
    queue_name="mi_cola",
    status="New",
    mark_as_processing=True
)

# Actualizar elemento con resultado
client.update_queue_item(
    item_id="550e8400-e29b-41d4-a716-446655440000",
    data={"result": "completed"},
    status="Successful",
    etapa="Procesamiento completado"
)

# Obtener analíticas
analytics = client.get_queue_analytics(period='24h')
```

### 📧 Gestión de Correos

```python
# Obtener correo por ID
email = client.get_email_by_id("email_123")

# Responder correo simple
result = client.reply_to_email(
    email_id="email_123",
    mensaje="Gracias por su consulta",
    tipo_respuesta="texto"
)

# Responder con adjuntos
with open("reporte.pdf", "rb") as f:
    archivo_data = f.read()

result = client.reply_to_email(
    email_id="email_123",
    mensaje="<p>Adjunto el reporte</p>",
    tipo_respuesta="html",
    archivos=[("reporte.pdf", archivo_data)]
)
```

## 💻 CLI (Línea de Comandos)

```bash
# Verificar versión
python -m kurai --version

# Health check
python -m kurai health-check --tenant-url https://api.cloud.lexia.la --api-key lx-xxxxx

# Listar áreas
python -m kurai list-areas --json

# Subir documento
python -m kurai upload invoice.pdf --area-id 1 --description "Factura enero"

# Agregar a cola
python -m kurai add-queue-item "processing" --data '{"task":"extract"}' --priority 2

# Ver analíticas
python -m kurai queue-analytics --period 7d
```

## 🛡️ Manejo de Errores

```python
from kurai import KuraiException, KuraiAuthenticationError

try:
    result = client.upload_document("/path/to/file.pdf", area_id=1)
except KuraiAuthenticationError:
    print("Error: API key inválida")
except KuraiException as e:
    print(f"Error de API: {e.message}")
    print(f"Código: {e.status_code}")
except FileNotFoundError:
    print("Error: Archivo no encontrado")
```

## 📖 Documentación Completa

### Métodos Disponibles

#### Documentos
- `upload_document(file_path, area_id, description="")` - Subir documento
- `upload_and_process_document(file_path, area_id, description="")` - Subir y procesar
- `get_document_extracted_data(document_id)` - Obtener datos extraídos
- `get_documents_extracted_data_batch(document_ids)` - Lote de datos extraídos
- `list_processed_documents(page=1, per_page=50, area_id=None, status=None)` - Listar procesados
- `get_document_url(document_id)` - Obtener URL del documento
- `bulk_delete_documents(document_ids)` - Eliminar múltiples

#### Colas
- `add_queue_item(queue_name, data, priority=0)` - Agregar elemento
- `get_next_queue_item(queue_name, status="New", priority_order=True, mark_as_processing=False)` - Obtener siguiente
- `update_queue_item(item_id, data=None, status=None, merge_mode="update", etapa=None)` - Actualizar elemento
- `bulk_delete_queue_items(item_ids)` - Eliminar múltiples
- `get_queue_analytics(period='24h')` - Obtener analíticas

#### Grids
- `get_grid_data(grid_id, page=1, per_page=50, filters=None)` - Obtener datos
- `get_grid_info(grid_id)` - Obtener información

#### Áreas
- `list_areas()` - Listar áreas disponibles

#### Correos
- `get_email_by_id(email_id)` - Obtener correo
- `reply_to_email(email_id, mensaje, tipo_respuesta="texto", asunto_personalizado=None, archivos=None)` - Responder

#### Utilidades
- `health_check()` - Verificar estado de la API

## 📊 Ejemplo Completo

```python
import kurai
from kurai import KuraiException

def flujo_completo():
    # Configurar cliente
    client = kurai.Client(
        tenant_url="https://api.cloud.lexia.la",
        api_key="lx-xxxxxxxxxxxxxxxxxxxxx"
    )
    
    try:
        # 1. Verificar conexión
        health = client.health_check()
        assert health['status'] == 'ok', "API no disponible"
        
        # 2. Obtener áreas
        areas = client.list_areas()
        area_id = areas['areas'][0]['id']
        
        # 3. Subir y procesar documento
        doc_result = client.upload_and_process_document(
            file_path="/path/to/invoice.pdf",
            area_id=area_id,
            description="Factura para procesamiento"
        )
        
        document_id = doc_result['document']['id']
        print(f"✅ Documento subido: {document_id}")
        
        # 4. Agregar a cola de procesamiento
        queue_result = client.add_queue_item(
            queue_name="document_processing",
            data={
                "document_id": document_id,
                "action": "extract_invoice_data"
            },
            priority=2
        )
        
        print(f"✅ Tarea en cola: {queue_result['item']['id']}")
        
        # 5. Obtener estadísticas
        analytics = client.get_queue_analytics("24h")
        print(f"📊 Procesados hoy: {analytics['summary']['processed_items']}")
        
    except KuraiException as e:
        print(f"❌ Error: {e.message}")

if __name__ == "__main__":
    flujo_completo()
```

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/lexia/kurai-sdk/issues)
- **Email**: [dev@lexia.la](mailto:dev@lexia.la)
- **Documentación**: [docs.lexia.la](https://docs.lexia.la)
- **Sitio web**: [lexia.la](https://lexia.la)

## 📄 Licencia

Copyright (c) 2024 Lexia SPA. Todos los derechos reservados.

Este software es propiedad de Lexia SPA y está protegido por derechos de autor. 
Ver [LICENSE](LICENSE) para más detalles.

---

**Desarrollado con ❤️ por [Lexia SPA](https://lexia.la)**

*Transformando el futuro del trabajo con automatización inteligente*