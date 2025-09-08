# 🚀 Kurai SDK

**Cliente oficial para la API pública de Lexia**

[![GitHub release](https://img.shields.io/github/release/lexia-dev/kurai-sdk.svg)](https://github.com/lexia-dev/kurai-sdk/releases)
[![Python versions](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lexia-dev/kurai-sdk.svg?style=social)](https://github.com/lexia-dev/kurai-sdk/stargazers)

Kurai es el SDK oficial en Python para interactuar con todos los endpoints públicos de la API de Lexia. Proporciona una interfaz simple y pythónica para integrar las funcionalidades de automatización y procesamiento de documentos de Lexia en tus aplicaciones.

## 📦 Instalación

### 🎯 Instalación desde GitHub (Recomendada)

```bash
# Instalar la última versión
pip install git+https://github.com/lexia-dev/kurai-sdk.git

# O instalar una versión específica
pip install git+https://github.com/lexia-dev/kurai-sdk.git@v1.0.0
```

### 🔄 Actualizar a la última versión

```bash
pip install --upgrade git+https://github.com/lexia-dev/kurai-sdk.git
```

### ✅ Verificar instalación

```bash
python -c "import kurai; print(f'✅ Kurai SDK v{kurai.__version__} instalado correctamente')"
```

### 📋 Requisitos

- **Python 3.7+**
- **requests** >= 2.25.0
- **pydantic** >= 1.8.0
- **click** >= 8.0.0

> 💡 **Nota**: Las dependencias se instalan automáticamente

## ⚡ Inicio Rápido (30 segundos)

```python
import kurai

# 1. Configurar cliente
client = kurai.Client(
    tenant_url="https://api.cloud.lexia.la",
    api_key="lx-xxxxxxxxxxxxxxxxxxxxx"
)

# 2. Verificar conexión
health = client.health_check()
print(f"✅ Estado: {health['status']}")

# 3. ¡Ya estás listo para usar todas las funcionalidades!
areas = client.list_areas()
print(f"📁 Áreas disponibles: {len(areas['areas'])}")
```

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

## 🔄 Actualizaciones y Versionado

### Obtener la última versión
```bash
pip install --upgrade git+https://github.com/lexia-dev/kurai-sdk.git
```

### Instalar versión específica
```bash
pip install git+https://github.com/lexia-dev/kurai-sdk.git@v1.0.0
```

### Ver historial de cambios
Consulta [CHANGELOG.md](CHANGELOG.md) o [GitHub Releases](https://github.com/lexia-dev/kurai-sdk/releases) para ver todas las actualizaciones.

## 🚀 Empezar Ahora

### Paso 1: Instalar
```bash
pip install git+https://github.com/lexia-dev/kurai-sdk.git
```

### Paso 2: Obtener API Key
1. Ve a tu panel de Lexia
2. Genera una nueva API Key
3. Copia la key (empieza con `lx-`)

### Paso 3: Probar la conexión
```python
import kurai

client = kurai.Client(
    tenant_url="https://api.cloud.lexia.la",
    api_key="lx-tu-api-key-aqui"
)

# Verificar que funciona
health = client.health_check()
print(f"✅ Conexión exitosa: {health['status']}")
```

### Paso 4: ¡Empezar a desarrollar!
```python
# Listar áreas disponibles
areas = client.list_areas()

# Subir un documento
result = client.upload_document("/path/to/file.pdf", area_id=1)

# Trabajar con colas
item = client.add_queue_item("mi_cola", {"task": "procesar"})
```

## 🎓 Tutoriales y Ejemplos

### 🏃‍♂️ Ejemplo Express (2 minutos)
```python
import kurai

# Configurar y probar
client = kurai.Client("https://api.cloud.lexia.la", "lx-xxxxx")
print("✅ SDK conectado:", client.health_check()['status'])

# Subir documento y agregarlo a cola
doc = client.upload_document("factura.pdf", area_id=1)
cola = client.add_queue_item("procesamiento", {"doc_id": doc['document']['id']})
print(f"📄 Documento {doc['document']['id']} en cola {cola['item']['id']}")
```

### 🏭 Ejemplo Productivo
```python
import kurai
import os
from pathlib import Path

def procesar_facturas():
    client = kurai.Client(
        tenant_url=os.getenv("LEXIA_URL"),
        api_key=os.getenv("LEXIA_API_KEY")
    )
    
    # Procesar todas las facturas de una carpeta
    facturas_dir = Path("./facturas")
    
    for archivo in facturas_dir.glob("*.pdf"):
        try:
            # Subir y procesar
            resultado = client.upload_and_process_document(
                str(archivo),
                area_id=1,
                description=f"Factura {archivo.name}"
            )
            
            # Agregar a cola de validación
            client.add_queue_item(
                "validacion_facturas",
                {
                    "document_id": resultado['document']['id'],
                    "filename": archivo.name,
                    "timestamp": resultado['document']['created_at']
                },
                priority=2
            )
            
            print(f"✅ {archivo.name} procesada correctamente")
            
        except Exception as e:
            print(f"❌ Error con {archivo.name}: {e}")

if __name__ == "__main__":
    procesar_facturas()
```

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/Kurai-software/Kurai_SDK/issues)
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