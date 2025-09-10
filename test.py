import kurai 

# Crear cliente
client = kurai.Client(
    tenant_url="https://api.cloud.lexia.la",
    api_key="lx-yucfi04YjEnJ6Jat285Fhbjj9QW59aKjCiFAUFWVxWOqc"
)

# Probar health check
try:
    health = client.health_check()
    print(f"✅ Health check exitoso: {health}")

    print("\n📝 Test 1: Obtener siguiente elemento (básico)")
    result = client.get_next_queue_item(
        queue_name="684e69fb-c078-441d-8bb3-c9b8e0be0226",
        status= "In Progress",                    # "New", "In Progress", "Successful", "Failed"  
        priority_order=True,             # Respetar prioridad
        mark_as_processing=True          # Marcar como "In Progress" automáticamente
    )
    print(f"Resultado: {result}")
except Exception as e:
    print(f"❌ Error: {e}")