#!/usr/bin/env python3
"""
CLI para Kurai SDK
==================

Interfaz de línea de comandos para interactuar con Lexia desde terminal.

Copyright (c) 2024 Lexia SPA. Todos los derechos reservados.

Uso:
    python -m kurai --version
    python -m kurai health-check
    python -m kurai upload file.pdf --area-id 1
"""

import argparse
import sys
import json
import os
from .client import Client
from .exceptions import KuraiException
from . import __version__


def print_json(data, title=None):
    """Helper para imprimir JSON formateado"""
    if title:
        print(f"\n{title}")
        print("-" * len(title))
    print(json.dumps(data, indent=2, ensure_ascii=False))


def create_client(args):
    """Crear cliente desde argumentos CLI"""
    tenant_url = args.tenant_url or os.getenv('LEXIA_TENANT_URL')
    api_key = args.api_key or os.getenv('LEXIA_API_KEY')
    
    if not tenant_url:
        print("❌ Error: Se requiere --tenant-url o variable LEXIA_TENANT_URL")
        sys.exit(1)
    
    if not api_key:
        print("❌ Error: Se requiere --api-key o variable LEXIA_API_KEY")
        sys.exit(1)
    
    return Client(tenant_url=tenant_url, api_key=api_key)


def cmd_health_check(args):
    """Verificar estado de la API"""
    try:
        client = create_client(args)
        health = client.health_check()
        
        if health['status'] == 'ok':
            print("✅ API funcionando correctamente")
            print_json(health, "Detalles")
        else:
            print("❌ API con problemas")
            print_json(health, "Detalles")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_list_areas(args):
    """Listar áreas disponibles"""
    try:
        client = create_client(args)
        areas = client.list_areas()
        
        if areas.get('areas'):
            print(f"✅ {len(areas['areas'])} áreas encontradas:")
            for area in areas['areas']:
                print(f"  - ID: {area['id']}, Nombre: {area['nombre']}")
        else:
            print("⚠️ No se encontraron áreas")
            
        if args.json:
            print_json(areas, "\nDatos completos")
            
    except KuraiException as e:
        print(f"❌ Error de API: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_upload_document(args):
    """Subir documento"""
    try:
        if not os.path.exists(args.file_path):
            print(f"❌ Error: Archivo no encontrado: {args.file_path}")
            sys.exit(1)
        
        client = create_client(args)
        
        if args.process:
            result = client.upload_and_process_document(
                file_path=args.file_path,
                area_id=args.area_id,
                description=args.description or ""
            )
            print("✅ Documento subido y en procesamiento")
        else:
            result = client.upload_document(
                file_path=args.file_path,
                area_id=args.area_id,
                description=args.description or ""
            )
            print("✅ Documento subido")
        
        doc = result.get('document', {})
        print(f"  ID: {doc.get('id')}")
        print(f"  Nombre: {doc.get('nombre')}")
        print(f"  Estado: {doc.get('status')}")
        
        if args.json:
            print_json(result, "\nDatos completos")
            
    except KuraiException as e:
        print(f"❌ Error de API: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_add_queue_item(args):
    """Agregar elemento a cola"""
    try:
        # Parsear datos JSON si se proporcionan
        data = {}
        if args.data:
            try:
                data = json.loads(args.data)
            except json.JSONDecodeError:
                print("❌ Error: --data debe ser JSON válido")
                sys.exit(1)
        
        client = create_client(args)
        result = client.add_queue_item(
            queue_name=args.queue_name,
            data=data,
            priority=args.priority
        )
        
        if result.get('success'):
            item = result.get('item', {})
            print("✅ Elemento agregado a cola")
            print(f"  ID: {item.get('id')}")
            print(f"  Cola: {item.get('queue_name')}")
            print(f"  Referencia: {item.get('reference')}")
            print(f"  Prioridad: {item.get('priority')}")
        else:
            print("❌ No se pudo agregar elemento")
        
        if args.json:
            print_json(result, "\nDatos completos")
            
    except KuraiException as e:
        print(f"❌ Error de API: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def cmd_get_queue_analytics(args):
    """Obtener analíticas de colas"""
    try:
        client = create_client(args)
        analytics = client.get_queue_analytics(period=args.period)
        
        if analytics.get('success'):
            summary = analytics.get('summary', {})
            print("📊 Analíticas de colas:")
            print(f"  Total elementos: {summary.get('total_items', 0)}")
            print(f"  Pendientes: {summary.get('pending_items', 0)}")
            print(f"  Procesados: {summary.get('processed_items', 0)}")
            print(f"  Fallidos: {summary.get('failed_items', 0)}")
            print(f"  Período: {analytics.get('period', 'N/A')}")
        else:
            print("❌ No se pudieron obtener analíticas")
        
        if args.json:
            print_json(analytics, "\nDatos completos")
            
    except KuraiException as e:
        print(f"❌ Error de API: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Función principal del CLI"""
    parser = argparse.ArgumentParser(
        prog='kurai',
        description='CLI para Kurai SDK - Cliente oficial de Lexia',
        epilog='Copyright (c) 2024 Lexia SPA. Todos los derechos reservados.'
    )
    
    # Argumentos globales
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'Kurai SDK {__version__}'
    )
    
    parser.add_argument(
        '--tenant-url',
        help='URL del tenant de Lexia (o usar LEXIA_TENANT_URL)'
    )
    
    parser.add_argument(
        '--api-key',
        help='API Key de Lexia (o usar LEXIA_API_KEY)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Mostrar respuesta completa en JSON'
    )
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # health-check
    subparsers.add_parser('health-check', help='Verificar estado de la API')
    
    # list-areas
    subparsers.add_parser('list-areas', help='Listar áreas disponibles')
    
    # upload
    upload_parser = subparsers.add_parser('upload', help='Subir documento')
    upload_parser.add_argument('file_path', help='Ruta al archivo a subir')
    upload_parser.add_argument('--area-id', type=int, required=True, help='ID del área donde subir')
    upload_parser.add_argument('--description', help='Descripción del documento')
    upload_parser.add_argument('--process', action='store_true', help='Procesar automáticamente después de subir')
    
    # add-queue-item
    queue_parser = subparsers.add_parser('add-queue-item', help='Agregar elemento a cola')
    queue_parser.add_argument('queue_name', help='Nombre de la cola')
    queue_parser.add_argument('--data', help='Datos JSON para el elemento')
    queue_parser.add_argument('--priority', type=int, choices=[0, 1, 2], default=0, help='Prioridad: 0=Low, 1=Medium, 2=High')
    
    # queue-analytics
    analytics_parser = subparsers.add_parser('queue-analytics', help='Obtener analíticas de colas')
    analytics_parser.add_argument('--period', choices=['24h', '7d', '30d'], default='24h', help='Período de análisis')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Ejecutar comando
    if args.command == 'health-check':
        cmd_health_check(args)
    elif args.command == 'list-areas':
        cmd_list_areas(args)
    elif args.command == 'upload':
        cmd_upload_document(args)
    elif args.command == 'add-queue-item':
        cmd_add_queue_item(args)
    elif args.command == 'queue-analytics':
        cmd_get_queue_analytics(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()