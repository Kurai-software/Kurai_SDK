import kurai

# Configurar cliente
client = kurai.Client(
    tenant_url="https://api.cloud.lexia.la",
    api_key="lx-e4og6Z6BNreKl3WTCYfBE0OaHRAJPjpvhd2QOWAUZs1Su"
)

# Test: Finalizar elemento simple
try:
    result = client.finish_queue_item(
        item_id="f0bd8930-0fdf-45e3-bcb6-d6c589d6c7ef"
    )
    print("Exitoso:")
    print(result)
except Exception as e:
    print(f"Error: {e}")