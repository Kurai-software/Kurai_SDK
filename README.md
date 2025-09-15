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

# NUEVO 🎯: Finalizar elemento automáticamente como "Successful"
result = client.finish_queue_item(
    item_id="ca9cf1c9-9d9b-4b24-8547-63d1c5265fbf",
    output={
        "resultado": "Documento procesado exitosamente",
        "datos_extraidos": {"total": "$1,500.00", "cliente": "Acme Corp"},
        "tiempo_procesamiento": "2.3 segundos",
        "precision": "99.2%"
    },
    etapa="Procesamiento completado"
)

# NUEVO 🎯: Finalizar simple (sin datos de salida)
result = client.finish_queue_item(
    item_id="550e8400-e29b-41d4-a716-446655440000"
)

# NUEVO 🎯: Finalizar con progreso personalizado
result = client.finish_queue_item(
    item_id="abc12345-def6-7890-abcd-123456789012",
    output={"status": "Completado con observaciones"},
    progress=95,
    etapa="Finalizado con advertencias"
)

# Obtener analíticas
analytics = client.get_queue_analytics(period='24h')
```

### 🎯 Flujo Completo de Cola con `finish_queue_item`

```python
import kurai

client = kurai.Client("https://api.cloud.lexia.la", "lx-xxxxx")

# 1. Obtener siguiente elemento para procesar
item = client.get_next_queue_item(
    queue_name="document_processing",
    status="New",
    mark_as_processing=True  # Marca automáticamente como "In Progress"
)

if item['success'] and item['item']:
    item_id = item['item']['id']
    item_data = item['item']['data']
    
    try:
        # 2. Procesar el elemento
        document_id = item_data['document_id']
        extracted_data = client.get_document_extracted_data(document_id)
        
        # 3. Realizar lógica de negocio
        processed_result = {
            "total_amount": extracted_data.get('total', 0),
            "vendor_name": extracted_data.get('vendor', 'N/A'),
            "processing_timestamp": "2024-01-15T10:30:00Z",
            "validation_score": 0.98
        }
        
        # 4. 🎯 Finalizar elemento exitosamente
        result = client.finish_queue_item(
            item_id=item_id,
            output={
                "status": "Procesado exitosamente",
                "extracted_data": processed_result,
                "processing_time": "1.8 segundos",
                "confidence": "98%"
            },
            etapa="Completado y validado"
        )
        
        print(f"✅ Elemento {item_id} finalizado exitosamente")
        
    except Exception as e:
        # En caso de error, actualizar status manualmente
        client.update_queue_item(
            item_id=item_id,
            status="Failed",
            data={"error": str(e)},
            etapa="Error en procesamiento"
        )
        print(f"❌ Error procesando {item_id}: {e}")
```

### 📧 Gestión de Correos

```python
# Obtener correo por ID
email = client.get_email_by_id("email_123")

# NUEVO: Enviar correo simple
result = client.send_simple_email(
    to="cliente@empresa.com",
    subject="Documento procesado exitosamente",
    body="<h2>¡Listo!</h2><p>Su documento ha sido procesado correctamente.</p>"
)

# NUEVO: Enviar correo completo con múltiples destinatarios
result = client.send_email(
    to=["user1@test.com", "user2@test.com"],
    cc=["supervisor@empresa.com"],
    bcc=["archivo@empresa.com"],
    subject="Reporte mensual de procesamiento",
    body="""
    <h2>Reporte Mensual</h2>
    <p>Estimado equipo,</p>
    <p>Adjunto el reporte de procesamiento de documentos del mes.</p>
    <ul>
        <li>✅ 1,247 documentos procesados</li>
        <li>✅ 98.5% de precisión</li>
        <li>✅ Tiempo promedio: 2.1 segundos</li>
    </ul>
    """,
    reply_to="noreply@empresa.com"
)

# NUEVO: Enviar correo con adjuntos
with open("reporte.pdf", "rb") as f:
    pdf_data = f.read()

with open("datos.csv", "rb") as f:
    csv_data = f.read()

result = client.send_email(
    to="director@empresa.com",
    subject="Documentos del proyecto",
    body="<p>Adjunto los documentos solicitados.</p>",
    archivos=[
        ("reporte_completo.pdf", pdf_data),
        ("datos_exportados.csv", csv_data)
    ]
)

# NUEVO: Enviar notificación usando plantillas
result = client.send_notification_email(
    to="usuario@ejemplo.com",
    template_type="document_processed",
    template_data={
        "document_name": "factura_enero.pdf",
        "processing_time": "1.8 segundos",
        "confidence_score": "99.2%"
    }
)

# Responder correo existente
result = client.reply_to_email(
    email_id="email_123",
    mensaje="Gracias por su consulta, hemos procesado su solicitud.",
    tipo_respuesta="texto"
)

# Responder con adjuntos
result = client.reply_to_email(
    email_id="email_123",
    mensaje="<p>Adjunto el reporte solicitado</p>",
    tipo_respuesta="html",
    archivos=[("reporte.pdf", pdf_data)]
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
- **🆕 `finish_queue_item(item_id, output=None, progress=100, etapa=None)`** - Finalizar como "Successful"

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

### 🆕 Método `finish_queue_item` - Detalles

El método `finish_queue_item` es una forma conveniente de marcar un elemento de cola como completado exitosamente. **Automáticamente**:

- ✅ Establece el status como "Successful"
- ✅ Registra timestamp de finalización
- ✅ Establece progreso a 100% (o valor personalizado)
- ✅ Combina datos de salida con información existente
- ✅ Calcula duración total del proceso

#### Parámetros:
- `item_id` (str): **Requerido.** ID del elemento de cola (UUID)
- `output` (dict): **Opcional.** Datos de salida del procesamiento
- `progress` (int): **Opcional.** Progreso del elemento (0-100%, por defecto 100%)
- `etapa` (str): **Opcional.** Descripción de la etapa (máximo 255 caracteres)

#### Casos de uso ideales:
- ✅ Finalizar procesamiento de documentos
- ✅ Completar tareas de automatización
- ✅ Marcar workflows como exitosos
- ✅ Registrar resultados de validación

#### Ejemplo avanzado:
```python
# Procesar documento y finalizar
document_id = 12345
extracted_data = client.get_document_extracted_data(document_id)

# Procesar datos...
validation_result = validate_invoice_data(extracted_data)

# Finalizar con resultados detallados
result = client.finish_queue_item(
    item_id="ca9cf1c9-9d9b-4b24-8547-63d1c5265fbf",
    output={
        "document_id": document_id,
        "validation_status": "approved",
        "extracted_fields": {
            "invoice_number": "INV-2024-001",
            "total_amount": 1500.00,
            "vendor": "Acme Corporation",
            "due_date": "2024-02-15"
        },
        "confidence_scores": {
            "invoice_number": 0.99,
            "total_amount": 0.98,
            "vendor": 0.97
        },
        "processing_metrics": {
            "extraction_time": "1.2s",
            "validation_time": "0.8s",
            "total_time": "2.0s"
        }
    },
    etapa="Factura procesada y validada exitosamente"
)

print(f"✅ Factura procesada: {result['item']['completed_at']}")
```

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
        
        item_id = queue_result['item']['id']
        print(f"✅ Tarea en cola: {item_id}")
        
        # 5. Simular procesamiento y finalizar
        # (En un escenario real, esto sería procesamiento asíncrono)
        extracted_data = client.get_document_extracted_data(document_id)
        
        # 6. 🆕 Finalizar elemento con resultados
        finish_result = client.finish_queue_item(
            item_id=item_id,
            output={
                "extraction_successful": True,
                "data_extracted": extracted_data,
                "processing_timestamp": "2024-01-15T10:30:00Z"
            },
            etapa="Procesamiento completado exitosamente"
        )
        
        print(f"✅ Elemento finalizado: {finish_result['item']['completed_at']}")
        
        # 7. Obtener estadísticas
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
pip install --upgrade git+https://github.com/Kurai-software/Kurai_SDK.git
```

### Instalar versión específica
```bash
pip install git+https://github.com/Kurai-software/Kurai_SDK.git@v1.0.1
```

### Ver historial de cambios
Consulta [CHANGELOG.md](CHANGELOG.md) o [GitHub Releases](https://github.com/Kurai-software/Kurai_SDK/releases) para ver todas las actualizaciones.

## 🚀 Empezar Ahora

### Paso 1: Instalar
```bash
pip install git+https://github.com/Kurai-software/Kurai_SDK.git
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

### 🏭 Ejemplo Productivo con Colas
```python
import kurai
import os
import time
from pathlib import Path

def worker_procesar_facturas():
    """Worker que procesa elementos de cola continuamente"""
    client = kurai.Client(
        tenant_url=os.getenv("LEXIA_URL"),
        api_key=os.getenv("LEXIA_API_KEY")
    )
    
    print("🚀 Worker iniciado - Procesando facturas...")
    
    while True:
        try:
            # Obtener siguiente elemento
            next_item = client.get_next_queue_item(
                queue_name="facturas_procesamiento",
                status="New",
                mark_as_processing=True
            )
            
            if not next_item['success'] or not next_item['item']:
                print("⏳ No hay elementos pendientes, esperando...")
                time.sleep(10)
                continue
            
            item = next_item['item']
            item_id = item['id']
            document_id = item['data']['document_id']
            
            print(f"📄 Procesando documento {document_id}...")
            
            # Obtener datos extraídos
            extracted_data = client.get_document_extracted_data(document_id)
            
            # Procesar lógica de negocio
            processed_result = {
                "invoice_number": extracted_data.get('numero_factura'),
                "total_amount": float(extracted_data.get('total', 0)),
                "vendor_name": extracted_data.get('proveedor'),
                "processed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            
            # 🎯 Finalizar elemento exitosamente
            result = client.finish_queue_item(
                item_id=item_id,
                output={
                    "status": "Procesado exitosamente",
                    "extracted_data": processed_result,
                    "processing_time": "2.1 segundos",
                    "confidence": "97.8%"
                },
                etapa="Factura procesada y validada"
            )
            
            print(f"✅ Factura {document_id} procesada exitosamente")
            
        except Exception as e:
            print(f"❌ Error procesando elemento: {e}")
            
            # Marcar como fallido si tenemos el item_id
            if 'item_id' in locals():
                try:
                    client.update_queue_item(
                        item_id=item_id,
                        status="Failed",
                        data={"error": str(e)},
                        etapa="Error en procesamiento"
                    )
                except:
                    pass
            
            time.sleep(5)

if __name__ == "__main__":
    worker_procesar_facturas()
```

### 🔄 Ejemplo con Retry Logic
```python
def procesar_con_reintentos():
    """Ejemplo de procesamiento con lógica de reintentos"""
    client = kurai.Client("https://api.cloud.lexia.la", "lx-xxxxx")
    
    max_reintentos = 3
    
    for intento in range(max_reintentos):
        try:
            # Obtener elemento
            item = client.get_next_queue_item(
                queue_name="documentos_complejos",
                mark_as_processing=True
            )
            
            if not item['success']:
                break
                
            item_id = item['item']['id']
            
            # Procesar...
            resultado = procesar_documento_complejo(item['item']['data'])
            
            # 🎯 Finalizar exitosamente
            client.finish_queue_item(
                item_id=item_id,
                output=resultado,
                etapa=f"Completado en intento {intento + 1}"
            )
            
            print(f"✅ Procesado exitosamente en intento {intento + 1}")
            break
            
        except Exception as e:
            print(f"❌ Intento {intento + 1} falló: {e}")
            
            if intento == max_reintentos - 1:
                # Último intento, marcar como fallido
                client.update_queue_item(
                    item_id=item_id,
                    status="Failed",
                    data={"error": str(e), "intentos": max_reintentos},
                    etapa="Falló después de múltiples intentos"
                )
            else:
                # Reintento, volver a "New"
                client.update_queue_item(
                    item_id=item_id,
                    status="New",
                    data={"reintentos": intento + 1},
                    etapa=f"Reintento {intento + 1}"
                )
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