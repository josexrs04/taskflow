# Guía de contribución

Bienvenido/a al equipo. Estas son las reglas del juego.

## Flujo de trabajo
1. Coge un issue asignado a ti (o pide que te asignen uno). Un issue = una persona.
2. Actualiza `main` y crea una rama desde ahí.
3. Haz commits pequeños y con sentido.
4. Abre un Pull Request (PR) **en borrador (draft)** pronto si quieres feedback temprano.
5. Cuando CI esté en verde y tengas el checklist completo, pásalo a "Ready for review".
6. Atiende los comentarios con nuevos commits (no hagas force-push mientras te revisan, salvo que se pida).
7. Quien revisa aprueba; se hace **Squash and merge**. Borra la rama.

## Nombres de rama
`tipo/numero-issue-descripcion-corta`
- `fix/12-sort-priority`
- `feat/15-export-csv`
- `chore/20-add-storage-tests`
- `hotfix/31-remove-token`

## Mensajes de commit (Conventional Commits)
`tipo(ámbito): descripción en imperativo`
- `fix(services): ordenar por prioridad numérica`
- `feat(cli): añadir comando export`
- `test(storage): cubrir carga de archivo inexistente`
- `docs: explicar instalación en el README`

Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`.

## Reglas
- Nada se mete directamente en `main`. Todo va por PR.
- Un PR hace una sola cosa y es pequeño (idealmente < 300 líneas).
- Todo bug arreglado lleva un test que lo habría detectado.
- **Nunca** subas secretos (tokens, contraseñas, claves). Si ocurre, avisa en el momento.
