#!/usr/bin/env bash
# Crea labels, milestone e issues del proyecto de práctica en TU repo.
# Requisitos: GitHub CLI (https://cli.github.com) y haber hecho `gh auth login`.
# Uso: ./scripts/setup_github.sh
set -euo pipefail

command -v gh >/dev/null || { echo "Instala GitHub CLI: https://cli.github.com"; exit 1; }
gh repo view >/dev/null 2>&1 || { echo "Ejecuta esto dentro de un repo ya subido a GitHub."; exit 1; }

echo "→ Creando labels..."
mk() { gh label create "$1" --color "$2" --description "$3" --force >/dev/null; }
mk bug              d73a4a "Algo no funciona"
mk enhancement      a2eeef "Nueva funcionalidad"
mk security         b60205 "Problema de seguridad"
mk urgent           e99695 "Atender primero"
mk "good first issue" 7057ff "Ideal para empezar"
mk documentation    0075ca "Documentación"
mk chore            fef2c0 "Mantenimiento"
mk discussion       cfd3d7 "Pendiente de decidir"

echo "→ Creando milestone..."
gh api repos/:owner/:repo/milestones -f title="v0.4.0" \
  -f description="Sprint 1: estabilidad y primeras mejoras" >/dev/null 2>&1 || true

new() { # título, labels, cuerpo
  gh issue create --title "$1" --label "$2" --milestone "v0.4.0" --body "$3" >/dev/null
  echo "   ✓ $1"
}

echo "→ Creando issues..."

new "El orden por prioridad no es correcto" "bug,good first issue" \
"**Qué ocurre**
\`taskflow list --by-priority\` no ordena de alta a baja.

**Pasos**
1. \`taskflow add A --priority low\`
2. \`taskflow add B --priority high\`
3. \`taskflow add C --priority medium\`
4. \`taskflow list --by-priority\`

**Esperado**: high, medium, low
**Actual**: high, low, medium

**Criterios de aceptación**
- [ ] Orden descendente por prioridad (high → low)
- [ ] Test que lo cubra"

new "Los IDs se reutilizan al borrar tareas" "bug" \
"Si creo 3 tareas, borro la #1 y creo otra, la nueva recibe el id #3 que ya existe → hay dos tareas con el mismo id y \`done\`/\`delete\` afectan a ambas.

Reproducir: add A, add B, add C, delete 1, add D, list.

**Criterios de aceptación**
- [ ] Los ids son siempre únicos
- [ ] Test de regresión"

new "Completar una tarea inexistente dice que ha ido bien" "bug" \
"\`taskflow done 999\` imprime 'Tarea #999 completada' y sale con código 0 aunque no exista.

**Esperado**: mensaje de error claro y código de salida distinto de 0.

> Nota de producto: no estoy segura de si \`delete\` debería comportarse igual. Dime qué opinas en un comentario antes de tocarlo."

new "SEGURIDAD: hay un token hardcodeado en config.py" "security,urgent" \
"En \`taskflow/config.py\` hay un token de la API de notificaciones en texto plano, y ya está en el historial de git.

**Qué hacer**
- [ ] Leer el token desde una variable de entorno
- [ ] Documentar la variable en el README
- [ ] Avisar en este issue de qué hay que hacer con el token ya expuesto (¿y con el historial?)

Prioridad máxima, va por rama \`hotfix/\`."

new "Filtrar tareas por fecha límite (--due-before)" "enhancement" \
"Como usuario quiero \`taskflow list --due-before 2026-12-31\` para ver solo lo que vence antes de esa fecha.

**Criterios de aceptación**
- [ ] Filtro en \`TaskService.list\` y flag en el CLI
- [ ] Fecha inválida → error claro
- [ ] Las tareas sin fecha NO aparecen cuando se usa el filtro
- [ ] Tests"

new "Mostrar solo tareas vencidas (--overdue)" "enhancement" \
"Como usuario quiero \`taskflow list --overdue\` para ver las tareas pendientes cuya fecha ya pasó.

**Criterios de aceptación**
- [ ] Solo tareas no completadas y con fecha < hoy
- [ ] Tests (ojo con depender de la fecha real)"

new "Exportar tareas a CSV" "enhancement" \
"Necesitamos \`taskflow export tareas.csv\`.

Columnas: id, title, priority, done, due.

> Pregunta abierta: ¿qué hacemos si el archivo ya existe? Propón algo en el PR."

new "Añadir tests para JsonStorage" "chore,good first issue" \
"Ahora mismo \`storage.py\` solo se prueba de rebote. Cubrir: archivo inexistente, guardar y cargar, archivo con JSON corrupto (decidir comportamiento)."

new "README: instalación y ejemplos de uso" "documentation,good first issue" \
"El README no explica cómo instalar ni usar la herramienta. Añadir: instalación, comandos con ejemplos, cómo ejecutar tests."

new "Decidir: ¿migrar de JSON a SQLite?" "discussion" \
"Con más usuarios, el JSON empieza a ser un cuello de botella (y no es seguro con accesos simultáneos).

**Esto NO es una tarea de código todavía.** Quiero que aportéis: pros/contras, esfuerzo estimado y vuestra recomendación en un comentario. Decidimos en la próxima reunión."

echo "Listo. Mira la pestaña Issues de tu repo."
