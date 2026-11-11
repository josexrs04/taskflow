# taskflow

Gestor de tareas en línea de comandos. Proyecto ficticio para practicar el trabajo en equipo con GitHub.

> El README está intencionadamente incompleto: es parte de un ticket 😉

## Instalación rápida
```bash
pip install -e ".[dev]"
pytest
```

## Configuración

Las notificaciones necesitan un token de API en la variable de entorno `NOTIFY_API_TOKEN`.
No lo escribas nunca en el código ni lo subas al repositorio.

PowerShell:
```powershell
$env:NOTIFY_API_TOKEN = "tu-token"
```

Bash:
```bash
export NOTIFY_API_TOKEN="tu-token"
```
