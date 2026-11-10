import os

# Configuración de la integración con el servicio de notificaciones.
NOTIFY_URL = "https://notify.example.com/api"
NOTIFICATION_API_TOKEN = os.environ.get("NOTIFICATION_API_TOKEN")
if not NOTIFICATION_API_TOKEN:
    raise RuntimeError("Falta configurar NOTIFICATION_API_TOKEN")
