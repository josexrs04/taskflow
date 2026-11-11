import os

# Configuración de la integración con el servicio de notificaciones.
NOTIFY_URL = "https://notify.example.com/api"
TOKEN_ENV_VAR = "NOTIFY_API_TOKEN"


def get_notify_token() -> str:
    """Devuelve el token de notificaciones o falla con un mensaje claro.

    Se lee al usarlo (no al importar el módulo) para que el resto de la
    herramienta funcione aunque no se haya configurado el token.
    """
    token = os.environ.get(TOKEN_ENV_VAR, "").strip()
    if not token:
        raise RuntimeError(
            f"Falta la variable de entorno {TOKEN_ENV_VAR}. "
            "Defínela antes de usar las notificaciones (ver README)."
        )
    return token
