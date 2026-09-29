# Instrucciones locales — Equipo 1 (Content, i18n & Proposals UI)

> **REVISIÓN REQUERIDA — no ejecutar prompts todavía.**  
> El plan de Equipo 1 (`PLAN-EQUIPO1.md`) está en semáforo **rojo** hasta que un PR de enmienda
> sea aprobado y fusionado por el profesor. No uses este archivo ni los prompts del plan para
> generar código de tareas mientras el plan no esté en verde. Ver comentario en
> [PR #28](https://github.com/ruvebal/ttod/pull/28#issuecomment-5876497526).

Contrato general del proyecto (del profesor, manda sobre este archivo si hay conflicto):
@AGENTS.md

---

## Nuestro módulo

Trabajamos solo en el frontend de contenido: navegación de citas ("wisdom"), i18n en/es y la
interfaz del formulario "proponer una cita". Hacemos UNA tarea por sesión: la que indique el
prompt. No adelantes trabajo de otras tareas aunque lo veas pendiente.

Archivos clave (verifica rutas y líneas antes de usarlas):
- services/frontend/src/pages/[locale]/wisdom/index.astro y [slug].astro
- services/frontend/src/content/wisdom.ts — fetchWisdom, frequencies(), labels
- services/frontend/src/types/domain.ts — WisdomEntry
- services/frontend/src/lib/auth.server.ts — requireUser, requireRole

## Límites (no negociables)

- NO modifiques services/backend/**, ttod.yml, cli.py ni ttod_core/**.
- NO edites AGENTS.md ni CLAUDE.md del repositorio.
- Los datos salen del payload que ya devuelve fetchWisdom: no crees endpoints nuevos.
- El endpoint de propuestas es del Equipo 5: lo consumimos, no lo implementamos.
- Reutiliza antes de escribir: frequencies(), labels, requireUser. Nada de contadores o
  filtros paralelos.
- requireUser: el Response se DEVUELVE desde el frontmatter, nunca se lanza.

## i18n

- El idioma sale de Astro.params.locale validado con isLocale().
- Todo texto de la interfaz, traducido en en y es. Nada fijo en inglés.
- Cada cita tiene su propio lang; la versión en otro idioma es otra entrada distinta
  (relation_type: translation_of). No inventes traducciones ni sufijos de ID.

## Componentes compartidos (no crees duplicados)

- src/components/EmptyState.astro — props: title, message, action? { label, href }
- src/components/Breadcrumbs.astro — props: locale, items: { label, href? }[] (último sin href)
- src/components/ProvenanceBlock.astro — recibe un WisdomEntry; muestra rights.holder,
  rights.license y origin con <dl>/<dt>/<dd>

En las páginas solo se importan y se colocan: cambios mínimos, otras tareas editan los mismos
archivos.

## Definición de Hecho (accesibilidad, en todo)

Operable por teclado · un nombre accesible o etiqueta · ningún significado solo por color ·
respeta prefers-reduced-motion.

## Testing

Doctrina Trophy, no Pyramid: la capa más barata que dé confianza real. Usa el framework que ya
tenga el proyecto. No cambies código de producción para hacer pasar un test.

## Git y pull requests

- Remotos: origin = nuestro fork (gontugithub/ttod), upstream = ruvebal/ttod. Los PR van a
  upstream main.
- Nombre de rama OBLIGATORIO: content-task<N>-<tema>, con N = número de la ficha
  (ASSIGNMENT-content-task<N>.md). Ej.: content-task1-browse-routes. El bot de revisión
  usa ese prefijo.
- Commits pequeños, Conventional Commits en inglés con scope content:
  feat(content): ..., fix(content): ..., test(content): ..., docs(content): ...
- NO hagas commit, push, merge ni abras PR sin que te lo pida explícitamente.
- NO modifiques services/frontend/src/types/domain.ts (contrato compartido entre equipos).
- Antes de dar una tarea por terminada, en services/frontend:
  npm run check && npm run build && npx vitest run
- El PR usa .github/pull_request_template.md completa, incluida la tabla de uso de IA
  ("qué hizo la IA / qué verificó el humano").

## Forma de trabajar

1. Explora y resume lo relevante.
2. Presenta un plan y ESPERA aprobación antes de escribir código.
3. Si falta información (p. ej. el contrato con el Equipo 5), pregunta; no la inventes.
4. Al terminar: cómo probarlo a mano en en y es, y un borrador de la sección "Uso de IA"
   para el PR (qué generaste tú y qué debe revisar el humano).
