# 🎯 Guía de práctica: trabajar en un proyecto real con GitHub

## La historia
Acabas de entrar como **desarrollador/a junior-mid** en el equipo de *taskflow*, una herramienta
interna de gestión de tareas. Tu **tech lead** (Claude) te asigna tickets, revisa tus PRs y te
mete algún marrón realista. Tú no decides la arquitectura ni haces merge sin revisión: ejecutas,
comunicas y mejoras.

---

## Fase 0 · Preparación (30 min)

1. Crea un repo **vacío** en tu GitHub (privado, nombre `taskflow`). Sin README ni .gitignore.
2. Descomprime el zip, entra en la carpeta y:
   ```bash
   git init -b main
   git add . && git commit -m "chore: estado inicial del proyecto"
   git remote add origin git@github.com:TU_USUARIO/taskflow.git
   git push -u origin main
   ```
3. Edita `.github/CODEOWNERS` y pon tu usuario. Haz commit **por PR** (primera práctica: ¡ya no empujes a main!).
   *Truco*: para este primer cambio, aún puedes pushear a main porque no has activado las protecciones.
4. Instala [GitHub CLI](https://cli.github.com), haz `gh auth login` y ejecuta:
   ```bash
   ./scripts/setup_github.sh
   ```
   Esto crea labels, milestone y **10 issues** (tu backlog).
5. Activa protección de rama: *Settings → Rules → Rulesets → New branch ruleset* sobre `main`:
   - Require a pull request before merging
   - Require status checks to pass (selecciona `test`, aparecerá tras la primera ejecución de CI)
   - Block force pushes
   - (Aprobaciones requeridas: ponlo a 0 si estás solo; la revisión la hace Claude en el chat)
6. Settings → General → Pull Requests: deja **solo "Allow squash merging"** y activa *Automatically delete head branches*.
7. Settings → Code security: activa **Dependabot alerts** y **Secret scanning**.
8. Prepara entorno local:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   pytest && ruff check .
   ```

✅ **Verifica**: Actions muestra CI en verde, intentas `git push origin main` y GitHub te lo rechaza.

---

## Fase 1 · Rutina diaria de un empleado (el ciclo que repetirás 100 veces)

```bash
git switch main && git pull                      # 1. partir de lo último
git switch -c fix/1-sort-priority                # 2. rama por ticket
# ... programas, pruebas ...
git add -p                                       # 3. revisa lo que añades
git commit -m "fix(services): ordenar por prioridad numérica"
git push -u origin HEAD                          # 4. sube la rama
gh pr create --draft --fill                      # 5. PR en borrador (o desde la web)
# ... CI en verde, checklist completo ...
gh pr ready                                      # 6. listo para revisar
```
Después: **pegadme el enlace o el diff del PR en el chat** y haré de revisor. Contestad a los
comentarios con commits nuevos. Cuando yo diga "LGTM", haces *Squash and merge*.

Antes de abrir cada PR, léete tú mismo el diff en GitHub como si fueras el revisor. Detectarás el 50 % de los problemas.

---

## Fase 2 · Sprint 1 (tu backlog)

Hazlos **en este orden recomendado**; en cada uno practicas algo distinto.

| # | Ticket | Qué practicas |
|---|--------|---------------|
| 4 | 🔥 Token hardcodeado | **Hotfix**, rama `hotfix/`, trabajo urgente, comunicar en el issue, rotar secretos, entender que el historial sigue conteniendo el token |
| 1 | Orden por prioridad | Tu primer PR "limpio": bug + test de regresión + Conventional Commits |
| 2 | IDs reutilizados | Reproducir primero con un test que falla (commit 1), luego el fix (commit 2) |
| 3 | Completar inexistente | Ticket ambiguo: **pregunta en el issue** antes de picar código |
| 8 | Tests de storage | PR de solo tests, buen primer contacto con el repo |
| 9 | README | PR de docs; revisar cómo se ve el Markdown en GitHub |
| 5 + 6 | `--due-before` y `--overdue` | **Conflicto de merge garantizado** (ver Fase 3) |
| 7 | Export CSV | Feature completa, decisiones de diseño explicadas en el PR |
| 10 | ¿SQLite? | Aportar opinión **por escrito** (pros/contras) sin escribir código |

Consejo: abre un PR por ticket, nunca mezcles dos tickets.

---

## Fase 3 · Situaciones "de empresa" que tienes que provocar y resolver

### 🔀 Conflicto de merge (tickets 5 y 6)
1. Crea `feat/5-due-before` y `feat/6-overdue` **ambas desde el mismo main**. Ambas tocan `list` en `services.py` y `cli.py`.
2. Abre los dos PRs. Haz merge del primero.
3. El segundo se marcará con conflictos. Resuélvelo **en local**:
   ```bash
   git switch feat/6-overdue
   git fetch origin && git rebase origin/main     # o git merge origin/main
   # resolver marcadores <<<<<<<, luego:
   git add . && git rebase --continue
   pytest
   git push --force-with-lease
   ```
   (`--force-with-lease` solo aquí, en TU rama de feature; nunca en main.)

### ⏪ Revert
Tras mergear algo, finge que rompió producción. Practica `gh pr` → botón **Revert** en GitHub, o:
```bash
git revert <sha-del-squash> && git push
```
Luego abre el PR correcto de nuevo.

### 🧹 Historial sucio
En una rama tuya haz 6 commits desordenados ("wip", "fix", "asdf") y límpialos con
`git rebase -i origin/main` (squash/reword) antes de pedir revisión.

### 🧯 "Me he equivocado de rama"
Haz un commit en `main` local por error. Recupéralo: `git switch -c mi-rama` + `git reset --hard origin/main` en main.
Luego practica `git reflog` para recuperar un commit "perdido".

### 📦 Stash y cambios de contexto
A mitad de tu ticket, llega algo urgente: `git stash`, cambias de rama, haces el hotfix, vuelves con `git stash pop`.

### 🍒 Cherry-pick
Crea una rama `release/0.3` desde un commit antiguo. Un fix posterior debe ir también ahí:
`git cherry-pick <sha>`.

### 🏷️ Release
Cuando termines el sprint: sube la versión a 0.4.0 en un PR, haz merge, y luego:
```bash
git tag -a v0.4.0 -m "Sprint 1"
git push origin v0.4.0
gh release create v0.4.0 --generate-notes
```
Cierra el milestone.

### 🤖 CI roto
Haz un PR que falle `ruff` a propósito (variable sin usar), lee el log de Actions, arréglalo.
Después, simula un test flaky: ¿cómo lo investigarías?

### 👀 Revisar el trabajo de otro (¡importante!)
Pídeme en el chat: **"Claude, dame un PR de un compañero para revisar"**. Te daré un diff con
problemas ocultos y tú escribirás los comentarios de revisión como lo harías en GitHub. Yo evalúo
tu revisión.

---

## Fase 4 · Cómo uso yo (Claude) este ejercicio contigo

Dime cualquiera de estas frases y cambio de rol:

- **"Standup"** → te pregunto qué hiciste ayer, qué harás hoy y bloqueos. Practicas comunicar.
- **"Revisa mi PR"** + pega el diff/enlace → reviso como tech lead (con comentarios por línea, nivel *blocking / suggestion / nit*).
- **"Dame un ticket nuevo"** → genero un issue realista (a veces ambiguo, a veces mal escrito).
- **"Hay un incidente"** → te lanzo un problema en "producción" y vemos cómo lo gestionas.
- **"Revisión de un compañero"** → te toca revisar a ti.
- **"Retro"** → analizamos qué fue bien y mal en el sprint.
- **"Entrevista técnica sobre Git"** → te pregunto cosas típicas de entrevista.

---

## Rúbrica de autoevaluación

Al final del sprint, ¿puedes decir que sí a todo?

- [ ] Todos mis PRs enlazan un issue (`Closes #N`) y son pequeños
- [ ] Ningún commit directo a `main`
- [ ] Todo bug lleva test de regresión
- [ ] Mensajes de commit coherentes
- [ ] He resuelto un conflicto, hecho un revert y un rebase interactivo
- [ ] He usado `--force-with-lease` solo en mi rama
- [ ] He tratado un secreto filtrado como una persona seria (rotar > borrar)
- [ ] He revisado un PR ajeno con comentarios útiles y amables
- [ ] He preguntado cuando el ticket era ambiguo, en vez de suponer
- [ ] He publicado un release con tag y notas

---

## Chuleta de comandos

```bash
git status / git log --oneline --graph --all
git diff / git diff --staged
git switch -c rama / git switch -
git restore archivo               # descarta cambios locales
git restore --staged archivo      # saca del staging
git commit --amend                # corrige el último commit (si no lo has subido)
git fetch --prune
git branch -d rama                # borrar rama local
gh pr list / gh pr checkout 12 / gh pr view --web / gh pr checks
gh issue list --assignee @me
```

¡Empieza por la **Fase 0** y cuéntame cuando tengas CI en verde! 🚀
