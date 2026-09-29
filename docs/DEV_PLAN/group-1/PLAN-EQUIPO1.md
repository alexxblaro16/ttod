# Equipo 1 — Content, i18n & Proposals UI

> **Estado del plan: REVISIÓN REQUERIDA — no ejecutar todavía.**  
> Este documento está en `main` como **borrador de proceso** (evidencia de planificación).  
> Un pase de revisión (Bugbot + profesor) encontró desajustes con el árbol actual de `main`.  
> **No abráis PRs de código de las tareas T1–T9 ni lancéis los prompts de Claude Code** hasta que:  
> (1) exista un PR de *enmienda* del plan que corrija los hallazgos,  
> (2) el profesor lo apruebe en GitHub (*Approve*), y  
> (3) ese PR esté fusionado en `main`.  
> Hasta entonces el semáforo del plan está en **rojo**. Las fichas canónicas de tarea mandan sobre este plan si chocan:  
> [`/teaching/tasks/`](https://ruvebal.github.io/ttod/teaching/assignments/) · hallazgos en el [comentario de #28](https://github.com/ruvebal/ttod/pull/28#issuecomment-5876497526).

Plan de trabajo del Equipo 1 (pareja) en el proyecto **TTOD — The Tao of Development**.
Recoge las 9 tareas con su detalle, el reparto entre **Persona A** y **Persona B**, el calendario del sprint y, en las tareas 1 a 6, un prompt listo para usar con Claude Code.

> Fuente canónica de cada tarea: `docs/DEV_PLAN/ASSIGNMENTS/ASSIGNMENT-content-taskN.md` en el repositorio `ruvebal/ttod` (y las páginas públicas enlazadas desde el tablero). Si este plan y esas fichas no coinciden, **mandan esas fichas**.

---

## Índice

1. [Contexto y numeración](#1-contexto-y-numeración)
2. [Reparto y calendario](#2-reparto-y-calendario)
3. [Reglas comunes a todas las tareas](#3-reglas-comunes-a-todas-las-tareas)
4. [Dependencias con otros equipos y plan B](#4-dependencias-con-otros-equipos-y-plan-b)
5. [Cómo usar los prompts de Claude Code](#5-cómo-usar-los-prompts-de-claude-code)
6. [Tarea 1 — Rutas por sección, etiqueta y nivel](#tarea-1--rutas-por-sección-etiqueta-y-nivel)
7. [Tarea 2 — Breadcrumbs](#tarea-2--breadcrumbs-en-todas-las-rutas-de-contenido)
8. [Tarea 3 — Estados vacío y de error](#tarea-3--estados-vacío-y-de-error)
9. [Tarea 4 — Formulario "proponer una cita"](#tarea-4--formulario-proponer-una-cita)
10. [Tarea 5 — Fuente, derechos y procedencia](#tarea-5--fuente-derechos-y-procedencia)
11. [Tarea 6 — Tests unitarios y de componente](#tarea-6--tests-unitarios-y-de-componente)
12. [Tarea 7 — PR en un módulo ajeno](#tarea-7--abrir-un-pr-en-un-módulo-que-no-es-nuestro)
13. [Tarea 8 — Revisión de un PR ajeno](#tarea-8--revisar-formalmente-un-pr-de-otro-módulo)
14. [Tarea 9 — Decisión de diseño documentada](#tarea-9--documentar-una-decisión-de-diseño-real)
15. [Checklist final antes de la defensa](#checklist-final-antes-de-la-defensa)

---

## 1. Contexto y numeración

Nuestro módulo cubre la navegación del contenido (las citas o *wisdom*), la internacionalización `en`/`es` y la interfaz para proponer citas nuevas.

**Aviso sobre la numeración.** El tablero de la web (`/teaching/assignments/`) lista 10 tareas para el Equipo 1. La nº 1 del tablero ("rutas localizadas de índice y detalle") es el hello-world que **ya existe** en la implementación de referencia y no tiene ficha. Las fichas `content-task1` … `content-task9` corresponden a las tareas 2 a 10 del tablero.

| Este README / ficha | Nº en el tablero | Tarea |
|---|---|---|
| T1 | 2 | Rutas por sección, etiqueta y nivel |
| T2 | 3 | Breadcrumbs |
| T3 | 4 | Estados vacío y de error |
| T4 | 5 | Formulario "proponer una cita" |
| T5 | 6 | Fuente, derechos y procedencia |
| T6 | 7 | Tests unitarios y de componente |
| T7 | 8 | PR en un módulo ajeno |
| T8 | 9 | Revisión de un PR ajeno |
| T9 | 10 | Decisión de diseño documentada |

Si una ficha menciona "Task 7" para el testing, está usando el número del tablero.

**Archivos clave del frontend** (verificad las rutas y números de línea, pueden haber cambiado):

- `services/frontend/src/pages/[locale]/wisdom/index.astro`: índice, ya llama a `fetchWisdom(locale)`.
- `services/frontend/src/pages/[locale]/wisdom/[slug].astro`: detalle.
- `services/frontend/src/content/wisdom.ts`: exporta `fetchWisdom`, `frequencies()` (≈ línea 31) y `labels`.
- `services/frontend/src/types/domain.ts`: tipo `WisdomEntry` (`section`, `tags`, `level`, `rights`, `origin`…).
- `services/frontend/src/lib/auth.server.ts`: `requireUser` (≈ línea 62) y `requireRole`.

---

## 2. Reparto y calendario

El sprint dura tres semanas de desarrollo; la tercera es un hackathon de 4 horas. Después vienen la Unidad 7 (rendimiento) y la defensa oral.

| Semana | Persona A | Persona B |
|---|---|---|
| **1 — Fundamentos** | **T1** rutas de facetas | **T2** breadcrumbs + cerrar el contrato con el Equipo 5 |
| **2 — Funcionalidades** | **T3** estados vacío/error + **T5** procedencia | **T4** formulario de propuesta |
| **3 — Hackathon** | **T6** (tests de rutas y `frequencies()`) + **T7** PR externo | **T6** (tests del formulario) + **T8** revisión |
| **Juntos** | **T9** decisión de diseño y preparación de la defensa | |

La lógica del reparto:

- A lleva routing, i18n y presentación del contenido. B lleva la integración con otros equipos, el formulario y la revisión.
- B cierra el contrato con el Equipo 5 porque es quien construye el formulario.
- En la T6, cada uno prueba lo que ha construido.
- **Los dos debéis poder defender cualquier tarea.** Revisad siempre los PR del otro.

### Evitar conflictos de merge

`index.astro` y `[slug].astro` los tocan T2, T3 y T5.

- Una rama por tarea: `feat/t1-facet-routes`, `feat/t2-breadcrumbs`, `feat/t3-empty-error-states`, `feat/t4-propose-form`, `feat/t5-provenance`, `test/t6-content-tests`.
- Ramas pequeñas y mergeadas pronto.
- La lógica va en componentes (`Breadcrumbs`, `EmptyState`, `ProvenanceBlock`). En las páginas solo se importan y se colocan.
- Avisad al otro antes de tocar un archivo compartido.

### Acuerdos del primer día

- [ ] Props de `<EmptyState />`, porque A lo necesita en T1 y se formaliza en T3. Propuesta: `title`, `message` y un `action` opcional (texto + href).
- [ ] Props de `<Breadcrumbs />`. Propuesta: `locale` e `items: { label: string; href?: string }[]`, donde el último elemento no lleva enlace.
- [ ] B abre el issue del contrato con el Equipo 5 (ver sección 4).

---

## 3. Reglas comunes a todas las tareas

**Definición de Hecho de accesibilidad** (se hereda en todas las tareas; en revisión se cita, no se reinventa):

- Operable por teclado.
- Un nombre accesible o etiqueta.
- Ningún significado transmitido solo por color.
- Respeta `prefers-reduced-motion`.

**Límites del módulo:**

- **No se toca `services/backend/**` ni `ttod.yml`.** Los datos salen del payload que ya devuelve `fetchWisdom`.
- El idioma sale de `Astro.params.locale` validado con `isLocale()`. Una ruta que funciona en `en` pero da 404 o muestra texto en inglés en `es` suspende la tarea.
- Se reutiliza lo que ya existe (`frequencies()`, `labels`, `requireUser`) antes de escribir algo nuevo.

**Testing:** se sigue la doctrina **Trophy, no Pyramid** (Unidad 5). Se elige la capa más barata que dé confianza real, y un test de integración de una ruta real vale más que un test unitario de algo que ya está probado.

**Uso de IA:** en cada PR (descripción o commit) se documenta:

- qué generó la IA;
- qué revisasteis y cambiasteis vosotros;
- qué decisiones tomasteis y por qué.

Según la Unidad 6, la IA puede comentar pero nunca aprobar ni mergear.

**Defensa oral:** tenéis que poder enseñar el código en vivo y justificar cada decisión. No mergeéis nada que no sepáis explicar.

---

## 4. Dependencias con otros equipos y plan B

| Qué necesitamos | De quién | Cuándo | ¿Bloquea? |
|---|---|---|---|
| Endpoint `POST /api/v1/proposals` (tarea 3 del Equipo 5) | Equipo 5 | Semana 1, marcado como prioridad | **Sí**, a la T4 |
| Login/sesión (`requireUser`) | Equipo 5 | Ya existe | No |
| Código de otros módulos para la T7 | Cualquiera | Ya hay código base | No |
| Un PR abierto de otro equipo para la T8 | Cualquiera | Semana 3 | Sí, a la T8 |

**Plan B si el endpoint del Equipo 5 no está listo:**

1. **Proponemos nosotros el contrato.** Su ficha les obliga a acordarlo con nosotros.
   - Leed `create_proposal` en `ttod_core/proposals.py` (≈ línea 251) y `proposal create` en `cli.py` (≈ línea 276). Ahí están los campos que necesitarán.
   - Abrid un issue en GitHub con el JSON propuesto y etiquetad al Equipo 5.
2. **Construimos el formulario contra un mock.** Toda la llamada va en una función `submitProposal(payload)`. Mientras no exista el endpoint, devuelve una respuesta simulada; cuando exista, solo cambia esa función.
3. **Manejamos que el endpoint falle o no exista** (404, 5xx, red) con un mensaje de error amable.
4. **No escribimos el endpoint nosotros.** Es tarea del Equipo 5.
5. **Reordenamos la semana 2** si hace falta: primero T3 y T5, y T4 al final.
6. **Si al final de la semana 1 no hay contrato, se avisa al profesor.**
7. **Para la T8:** pactad pronto con otro equipo una revisión cruzada ("revisáis uno nuestro y revisamos uno vuestro").

### Contrato acordado con el Equipo 5 (rellenar)

```
Endpoint:        POST ______________________
Autenticación:   cookie de sesión (requireUser) — confirmar
Cuerpo (JSON):
{
  "________": "string",   // texto de la cita
  "________": "string",   // sección
  "________": "string",   // fuente
  ...
}
Respuesta OK:    201 Created → { "id": "..." }   — confirmar
Errores:         401 sin sesión · 400/422 validación · ______
Acordado el:     ____/____/______  en el issue #____
```

---

## 5. Cómo usar los prompts de Claude Code

1. Cread la rama de la tarea antes de abrir Claude Code.
2. Pegad el prompt tal cual. Todos piden a Claude Code que **explore primero y presente un plan antes de escribir código**. Leed el plan, corregidlo si hace falta y solo entonces aprobadlo.
3. Revisad cada diff. Si no entendéis algo, preguntadle a Claude Code por qué, antes de aceptarlo.
4. Probad a mano en `en` y en `es` antes de abrir el PR.
5. Añadid al PR la sección de uso de IA (ver sección 3).

Los prompts citan rutas y números de línea de las fichas, que pueden haber cambiado. Por eso piden a Claude Code que lo compruebe.

---

## Tarea 1 — Rutas por sección, etiqueta y nivel

| | |
|---|---|
| **Responsable** | Persona A |
| **Semana** | 1 |
| **Verbo** | find |
| **Depende de** | Nada |
| **Desbloquea** | T2 (breadcrumbs en facetas), T3, T5 (procedencia en listados) |
| **Lección** | Unidad 3 — Astro avanzado (colecciones, i18n, data fetching) |

### Objetivo

Tres rutas dinámicas nuevas que filtran las citas que ya trae `fetchWisdom(locale)`:

- `/{locale}/wisdom/sections/{section}/`
- `/{locale}/wisdom/tags/{tag}/`
- `/{locale}/wisdom/levels/{level}/`

Deben funcionar en `en` y en `es`.

### Punto de partida

- `index.astro` y `[slug].astro` ya muestran datos reales. Esta tarea **extiende su patrón**, no empieza de cero.
- `frequencies(entries, field)` con `field: 'section' | 'level' | 'tags'` ya está escrita en `wisdom.ts`, pero ninguna ruta la llama.
- Las tres rutas no existen porque el profesor las quitó a propósito.

### Qué hay que hacer

1. Crear las tres rutas dinámicas.
2. En cada una, llamar a `frequencies()` para obtener la lista de valores de la faceta y sus conteos.
3. Filtrar el `WisdomEntry[]` ya descargado:
   - `section` igual al parámetro;
   - `tags` que incluya el parámetro;
   - `level` igual al parámetro.
4. Mostrar la lista de facetas (pills, lista o lo que queráis) con enlaces a las otras facetas.
5. Poner un enlace simple de vuelta al índice. El componente completo de breadcrumbs es la T2.
6. Mostrar un estado vacío (no una página en blanco) cuando una faceta no tiene coincidencias en ese idioma.

### Criterios de aceptación

- [ ] `/{locale}/wisdom/sections/{section}/` funciona en `en` y `es` y lista las entradas con esa sección.
- [ ] `/{locale}/wisdom/tags/{tag}/` funciona en `en` y `es` y lista las entradas que incluyen esa etiqueta.
- [ ] `/{locale}/wisdom/levels/{level}/` funciona en `en` y `es` y lista las entradas con ese nivel.
- [ ] El índice y el detalle siguen mostrando datos reales en cualquier idioma que tenga entradas.
- [ ] Una faceta sin resultados muestra un estado vacío.

### Criterios de calidad

- **Reutilizar, no reinventar.** Se llama a `frequencies()`. Un contador de facetas hecho a mano junto a un import sin usar de `frequencies()` es un fallo de calidad, no un detalle de estilo.
- **i18n estructural.** El idioma sale de `Astro.params.locale` + `isLocale()`, y los textos de la interfaz no quedan fijos en inglés.
- **Test.** Al menos un test de integración o de componente que compruebe que una ruta de faceta real muestra datos filtrados reales. La T6 lo formaliza.
- **Accesibilidad:** la Definición de Hecho heredada.

### Defensa oral

- Señalar la línea exacta donde se llama a `frequencies()`.
- Explicar por qué se filtra sobre el payload ya descargado y no con un endpoint nuevo: el módulo no puede tocar `services/backend/**`.
- Enseñar el estado vacío en vivo.

### Prompt para Claude Code

```text
Contexto: trabajo en el proyecto TTOD (Astro), en el módulo de contenido del
Equipo 1. Tarea: crear tres rutas de navegación por faceta para las citas
("wisdom"):
  /{locale}/wisdom/sections/{section}/
  /{locale}/wisdom/tags/{tag}/
  /{locale}/wisdom/levels/{level}/
Deben funcionar en los idiomas en y es.

Antes de escribir código, explora y resume:
1. services/frontend/src/pages/[locale]/wisdom/index.astro y [slug].astro:
   cómo obtienen el locale (Astro.params.locale, isLocale()), cómo llaman a
   fetchWisdom(locale), cómo manejan las traducciones de la interfaz y si el
   proyecto usa getStaticPaths (salida estática) o SSR.
2. services/frontend/src/content/wisdom.ts: firma y comportamiento exactos de
   frequencies(entries, field) (debería estar cerca de la línea 31) y qué
   exporta labels.
3. services/frontend/src/types/domain.ts: el tipo WisdomEntry (section, tags,
   level).
4. Dónde están las cadenas traducidas de la interfaz y cómo se añaden nuevas.
5. Qué framework de tests se usa y dónde viven los tests.
Después, preséntame un plan (archivos a crear, cómo se generan las rutas, dónde
se llama a frequencies()) y ESPERA a que lo apruebe.

Requisitos de implementación:
- Crea las tres rutas dinámicas siguiendo el mismo patrón que index.astro.
- En cada ruta llama a frequencies() para obtener los valores de la faceta y
  sus conteos. NO escribas un contador propio ni dupliques esa lógica.
- Filtra el WisdomEntry[] que ya devuelve fetchWisdom(locale): section === param,
  tags.includes(param), level === param. No crees endpoints nuevos.
- Muestra una lista de facetas (con conteos) que enlace a las demás facetas del
  mismo tipo, respetando el prefijo /{locale}/.
- Añade un enlace simple de vuelta a /{locale}/wisdom/ (NO un componente de
  breadcrumbs: eso es otra tarea).
- Si una faceta no tiene coincidencias en ese idioma, muestra un estado vacío
  con texto traducido, nunca una página en blanco. Si existe un componente
  EmptyState en el proyecto, úsalo; si no, crea uno mínimo en
  src/components/EmptyState.astro con props title, message y action opcional
  ({ label, href }).
- Si el parámetro de idioma no es válido, compórtate igual que las rutas
  existentes.
- Todo el texto de la interfaz, traducido en en y es.
- Accesibilidad: HTML semántico, encabezados en orden, enlaces con texto
  descriptivo, operable por teclado, nada comunicado solo por color, respeta
  prefers-reduced-motion si añades transiciones.

Restricciones:
- No modifiques nada en services/backend/** ni ttod.yml.
- No cambies el comportamiento de index.astro ni [slug].astro salvo que sea
  imprescindible; si lo es, explícame por qué antes.

Tests:
- Añade al menos un test de integración/componente que compruebe que una ruta
  de faceta real muestra solo las entradas filtradas, y otro para el estado
  vacío. Usa el framework que ya tenga el proyecto. No añadas un test unitario
  de frequencies() si ya existe.

Al terminar:
- Dime cómo probarlo a mano (URLs concretas en en y es, incluida una faceta
  vacía).
- Resume, para la defensa oral: dónde está cada llamada a frequencies(), por
  qué se filtra en el cliente del payload existente y cómo se maneja el idioma.
- Redacta un borrador de la sección "Uso de IA" para el PR.
```

---

## Tarea 2 — Breadcrumbs en todas las rutas de contenido

| | |
|---|---|
| **Responsable** | Persona B |
| **Semana** | 1 |
| **Verbo** | keep |
| **Depende de** | T1 para integrarlo en las facetas (el componente se puede hacer antes) |
| **Lección** | Resultados de aprendizaje §4 del módulo (HTML semántico, i18n) |

### Objetivo

Que el índice, las facetas y el detalle muestren un camino claro de vuelta, del tipo **Wisdom → Faceta → Detalle**, en lugar de depender del botón atrás del navegador.

### Punto de partida

- `index.astro` y `[slug].astro` muestran contenido pero no tienen rastro de navegación.
- `labels` en `wisdom.ts` sirve para convertir slugs en nombres legibles y traducidos.
- `section`, `tags` y `level` de `WisdomEntry` definen los niveles de la jerarquía.

### Qué hay que hacer

1. Diseñar la jerarquía según la estructura real de rutas:
   - índice → `Wisdom`;
   - faceta → `Wisdom › {Faceta}`;
   - detalle → `Wisdom › {Sección} › {Cita}`.
2. Crear un único componente reutilizable, `src/components/Breadcrumbs.astro`.
3. Integrarlo en el índice, en las tres facetas y en el detalle.
4. Usar HTML semántico: `<nav aria-label="…">` + `<ol>` + `<li>`.

### Criterios de aceptación

- [ ] Breadcrumbs presentes en el índice, en las rutas de sección, etiqueta y nivel, y en el detalle.
- [ ] Todos los enlaces conservan el prefijo `/{locale}/` en `en` y `es`.
- [ ] Estructura `<nav>` con `aria-label` y `<ol>`.
- [ ] El último elemento lleva `aria-current="page"` y no es un enlace.

### Criterios de calidad

- **Un solo componente.** Nada de HTML de breadcrumbs duplicado en las páginas.
- **Accesibilidad:** la Definición de Hecho heredada, con `aria-label` en el `<nav>`.
- **Tests:** los enlaces resuelven bien en ambos idiomas y `aria-current="page"` está en el último elemento.

### Defensa oral

- Por qué un componente compartido y no HTML en línea.
- Cómo maneja las distintas profundidades: índice, faceta y detalle.

### Prompt para Claude Code

```text
Contexto: proyecto TTOD (Astro), módulo de contenido del Equipo 1. Tarea: un
componente de breadcrumbs compartido para todas las rutas de contenido
("wisdom"), en los idiomas en y es.

Antes de escribir código, explora y resume:
1. services/frontend/src/pages/[locale]/wisdom/: qué rutas existen (index,
   [slug] y, si ya están, las de facetas sections/tags/levels) y qué datos
   tiene cada una disponible.
2. services/frontend/src/content/wisdom.ts: qué exporta labels y cómo
   convierte slugs de section/level/tag en nombres legibles por idioma.
3. services/frontend/src/types/domain.ts: WisdomEntry (section, tags, level).
4. Cómo se traducen las cadenas de la interfaz.
5. Si existe algún layout común donde tenga sentido colocar el componente.
Después, preséntame un plan con la API del componente y la jerarquía por tipo
de página, y ESPERA a que lo apruebe.

Requisitos:
- Crea UN componente reutilizable, src/components/Breadcrumbs.astro, con esta
  API (ajústala solo si lo justificas):
    locale: string
    items: { label: string; href?: string }[]   // el último sin href
- Jerarquía:
    índice:  Wisdom
    faceta:  Wisdom › {nombre legible de la faceta}
    detalle: Wisdom › {sección de la cita, enlazada a su faceta} › {cita}
- Los nombres legibles salen de labels; no pongas traducciones a mano en las
  páginas.
- Todos los href llevan el prefijo /{locale}/ correcto.
- HTML semántico: <nav aria-label="..."> (etiqueta traducida) con <ol> y <li>.
  El último elemento lleva aria-current="page" y no es enlace. Los separadores
  visuales son decorativos (CSS o aria-hidden), no texto que lea el lector de
  pantalla.
- Integra el componente en index, [slug] y en las rutas de facetas si existen.
  Si las facetas aún no existen, deja el componente listo y dime exactamente
  qué línea añadir en cada una.
- En las páginas solo se importa el componente y se le pasan los items; nada
  de HTML de breadcrumbs duplicado.
- Si las rutas de facetas tenían un enlace simple de "volver al índice",
  sustitúyelo por el componente.
- Accesibilidad: operable por teclado, foco visible, nada comunicado solo por
  color, respeta prefers-reduced-motion si hay transiciones.

Restricciones:
- No toques services/backend/** ni ttod.yml.
- Cambios mínimos en los archivos de páginas, que otras tareas también editan.

Tests (con el framework que ya tenga el proyecto):
- El componente genera los enlaces correctos para en y para es.
- El último elemento tiene aria-current="page" y no es un enlace.
- Hay un <nav> con aria-label y una <ol>.

Al terminar:
- Dime cómo probarlo a mano en las tres profundidades y en ambos idiomas.
- Resume, para la defensa oral: por qué un componente compartido y cómo
  maneja las distintas profundidades.
- Redacta un borrador de la sección "Uso de IA" para el PR.
```

---

## Tarea 3 — Estados vacío y de error

| | |
|---|---|
| **Responsable** | Persona A |
| **Semana** | 2 |
| **Verbo** | keep |
| **Depende de** | T1 (reutiliza su `EmptyState`) |
| **Lección** | Unidad 5 (casos límite y fallos) y Unidad 3 |

### Objetivo

Que nunca aparezca una página en blanco ni un stack trace:

- una faceta o un índice sin entradas muestra un estado vacío con estilo;
- si el backend no responde, el usuario ve un mensaje legible y traducido.

### Punto de partida

Ahora mismo `index.astro` recorre las entradas directamente, sin comprobar nada. Si el array viene vacío o `fetchWisdom` falla, la página se queda en blanco o lanza una excepción. El "ejemplo" de esta tarea es precisamente la **ausencia** de esa protección.

### Qué hay que hacer

1. Diseñar **un** patrón de estado vacío acorde con el sistema de diseño (colores, tipografía, espaciado). Partid del `EmptyState` de la T1.
2. Aplicarlo al índice cuando `entries.length === 0`.
3. Aplicarlo al detalle cuando el `slug` no existe en el payload de ese idioma.
4. Envolver `fetchWisdom` en un `try/catch` (o usar el manejo de errores de Astro).
5. Mostrar el error traducido en `en` y `es`.
6. Que los estados vacío y de error sean accesibles.

### Criterios de aceptación

- [ ] `fetchWisdom` devuelve `[]` → el índice muestra un estado vacío con estilo.
- [ ] Un slug inexistente en ese idioma → "no encontrado" con estilo, sin crash.
- [ ] `fetchWisdom` lanza un error → mensaje traducido, sin stack trace.
- [ ] Ambos estados se ven en el idioma correcto.
- [ ] Sin regresiones: con datos, todo se ve como antes.

### Criterios de calidad

- **DRY:** un componente o partial reutilizable, no lógica duplicada en cada ruta.
- **Documentación del proceso:** en el PR, explicar por qué `try/catch` o por qué `error.astro`.
- **Tests:** mocks de `fetchWisdom` que devuelvan `[]` y que lancen un error, comprobando que aparece el mensaje traducido correcto.
- **Accesibilidad:** la Definición de Hecho heredada.

### Defensa oral

- Por qué un estado "no encontrado" dentro del componente en vez de una 404 del servidor en el detalle, o al revés si elegís la 404. Es importante saber qué código HTTP devuelve vuestra solución.
- Ventajas e inconvenientes de capturar errores en cada ruta frente al manejo global de Astro.

### Prompt para Claude Code

```text
Contexto: proyecto TTOD (Astro), módulo de contenido del Equipo 1. Tarea:
manejo de estados vacío y de error en las rutas de contenido ("wisdom"), en en
y es. Objetivo: nunca una página en blanco ni un stack trace.

Antes de escribir código, explora y resume:
1. services/frontend/src/content/wisdom.ts: cómo funciona fetchWisdom(locale),
   qué devuelve y cómo falla (errores de red, respuestas no-OK).
2. services/frontend/src/pages/[locale]/wisdom/index.astro, [slug].astro y las
   rutas de facetas (sections/tags/levels) si existen: dónde se asume que hay
   datos.
3. Si existe src/components/EmptyState.astro (lo pudo crear otra tarea) y su
   API actual.
4. El sistema de diseño: variables CSS, tipografía y espaciados usados.
5. Si el proyecto usa salida estática o SSR, y si existe una página de error
   de Astro (404.astro / 500.astro).
6. Cómo se traducen las cadenas de la interfaz.
Después, preséntame un plan que incluya: la decisión try/catch frente a la
página de error de Astro (con pros y contras), qué código HTTP devolverá el
detalle cuando el slug no existe, y los archivos a tocar. ESPERA a que lo
apruebe.

Requisitos:
- Un único patrón reutilizable de estado vacío (reutiliza o amplía EmptyState;
  no crees un segundo componente parecido) y un estado de error reutilizable
  (puede ser una variante del mismo componente).
- Índice: si entries.length === 0, muestra el estado vacío.
- Detalle: si el slug no está en el payload del idioma actual, muestra un
  estado "no encontrado" con enlace de vuelta al índice del mismo idioma.
- Facetas: usa el mismo patrón para cero resultados.
- Envuelve las llamadas a fetchWisdom para que un fallo de red o una respuesta
  no-OK muestre un mensaje legible y traducido, nunca un stack trace. No
  dupliques el try/catch en cada página si puedes centralizarlo con claridad.
- Todos los textos en en y es, según Astro.params.locale.
- Accesibilidad: el mensaje es texto real con un encabezado adecuado, el enlace
  de acción es operable por teclado, nada se comunica solo por color, respeta
  prefers-reduced-motion. Considera role="alert" solo para el error, no para el
  estado vacío.
- Sin regresiones: con datos, las rutas se ven exactamente igual que antes.

Restricciones:
- No toques services/backend/** ni ttod.yml.
- Cambios mínimos en las páginas, que otras tareas también editan.

Tests (con el framework que ya tenga el proyecto, mockeando fetchWisdom):
- Devuelve [] → aparece el estado vacío traducido (en y es).
- Lanza un error → aparece el mensaje de error traducido y no hay stack trace.
- Slug inexistente → aparece "no encontrado".
- Con datos → se muestran las entradas (sin regresión).

Al terminar:
- Dime cómo reproducir cada estado a mano (por ejemplo, cómo simular que el
  backend está caído en local).
- Redacta la nota de decisión para el PR (try/catch frente a error.astro, y
  por qué).
- Resume, para la defensa oral, las ventajas e inconvenientes de la opción
  elegida.
- Redacta un borrador de la sección "Uso de IA" para el PR.
```

---

## Tarea 4 — Formulario "proponer una cita"

| | |
|---|---|
| **Responsable** | Persona B |
| **Semana** | 2 (el contrato se cierra en la semana 1) |
| **Verbo** | contribute |
| **Depende de** | **Endpoint del Equipo 5** (dependencia fuerte). Ver sección 4 |
| **Áreas** | Content y Accounts |

### Objetivo

- Un usuario con sesión iniciada ve un formulario "Proponer una cita" con texto, sección y fuente.
- Al enviarlo, recibe un estado de "Éxito" o "Pendiente de revisión".
- Sin sesión, ve una invitación a iniciarla, no un formulario roto ni un 403.

### Punto de partida

- `requireUser` en `lib/auth.server.ts` (≈ línea 62) es el patrón de control de acceso. Se ejecuta en el frontmatter y **devuelve** un `Response`, no lo lanza (lanzarlo da un 500 en Astro 5).
- Los campos del formulario siguen la estructura de `WisdomEntry`.
- El backend reutilizará `create_proposal` de `ttod_core/proposals.py`. Nunca escribe directamente en `ttod.yml`: la cita solo se publica tras revisión humana.

### Qué hay que hacer

1. **Coordinarse con el Equipo 5** para fijar la URL y el JSON exactos. No hay que adivinar el contrato: se apunta en la sección 4.
2. **Control de sesión:** sin sesión, mensaje "Inicia sesión para proponer una cita" con enlace al login.
3. **Formulario** con HTML semántico: `<form>`, `<label>`, `<input>`/`<textarea>`/`<select>`.
4. **Validación en cliente:** campos obligatorios y longitudes básicas, sin llegar a la red si hay errores.
5. **Envío:** desactivar el botón, mostrar "Enviando…", hacer el `POST` y gestionar el éxito o el error.

### Criterios de aceptación

- [ ] El formulario no es visible ni usable sin sesión, y el control con `requireUser` funciona.
- [ ] El `POST` lleva exactamente los campos acordados.
- [ ] Un formulario vacío o incompleto muestra errores y **no** hace petición de red.
- [ ] Estados visuales distintos para "Enviando", "Éxito" y "Error".
- [ ] No se modifica `services/backend/**` ni `ttod.yml`.

### Criterios de calidad

- **Organización:** la lógica del formulario va en un componente o script propio, con el control de sesión y el envío separados.
- **Documentación:** el contrato acordado con el Equipo 5 aparece en la descripción del PR (es crítico en tareas entre equipos).
- **Tests:** mocks de `fetch` y `requireUser`, comprobando el payload correcto al enviar y que la validación bloquea el envío. Si es viable, un test de integración de que el formulario se oculta sin sesión.
- **Accesibilidad:**
  - `<label>` en cada campo;
  - errores enlazados con `aria-describedby`;
  - el éxito anunciado con `aria-live="polite"`;
  - más la Definición de Hecho heredada.

### Defensa oral

- Por qué se coordinó con el Equipo 5 antes de construir.
- Cómo se resolvió el caso sin sesión sin romper la experiencia.
- Validación en cliente frente a confiar solo en la del servidor.

### Prompt para Claude Code

> Antes de usarlo, rellenad el bloque CONTRATO con lo acordado en la sección 4. Si aún no hay contrato, dejad `PENDIENTE` y Claude Code trabajará contra un mock.

```text
Contexto: proyecto TTOD (Astro), módulo de contenido del Equipo 1. Tarea: la
interfaz del formulario "Proponer una cita". El endpoint lo construye OTRO
equipo (Equipo 5); nosotros solo lo consumimos.

CONTRATO acordado con el Equipo 5:
  Endpoint: POST <RELLENAR o PENDIENTE>
  Cuerpo JSON: <RELLENAR o PENDIENTE>
  Respuesta OK: <RELLENAR, p. ej. 201 { id }>
  Errores: <RELLENAR, p. ej. 401 sin sesión, 400/422 validación>

Antes de escribir código, explora y resume:
1. services/frontend/src/lib/auth.server.ts: cómo funciona requireUser (cerca
   de la línea 62), qué devuelve y cómo se usa en
   services/frontend/src/pages/[locale]/account/index.astro. Ojo: en Astro el
   Response se DEVUELVE desde el frontmatter, no se lanza.
2. services/frontend/src/types/domain.ts: WisdomEntry, para alinear los campos.
3. Si ya existe algún endpoint de propuestas en el frontend (p. ej. en
   src/pages/api/) y qué espera.
4. Cómo se traducen las cadenas de la interfaz y cómo se crean islas/scripts
   de cliente en este proyecto.
5. Qué framework de tests se usa.
Después, preséntame un plan: dónde vivirá el formulario (página dedicada
enlazada desde las rutas de wisdom o componente embebido), cómo separas el
control de sesión del envío y la estructura de archivos. ESPERA a que lo
apruebe.

Requisitos:
- Control de sesión en el servidor: si no hay usuario, NO se renderiza el
  formulario; se muestra "Inicia sesión para proponer una cita" (traducido)
  con enlace al login del mismo idioma. Nunca un 403 ni un formulario roto.
  No redirijas automáticamente si eso rompe la navegación; explícame la
  opción que elijas.
- Formulario semántico con campos: texto de la cita, sección y fuente (y los
  demás del contrato). Cada campo con su <label>.
- Validación en cliente: obligatorios y longitudes razonables. Si hay errores,
  NO se hace la petición. Cada error enlazado a su campo con
  aria-describedby, y el foco va al primer campo con error.
- Envío: toda la llamada en una única función submitProposal(payload) en su
  propio módulo. Si el contrato está PENDIENTE, que esa función use un mock
  claramente marcado (TODO) que simule éxito y error, para que luego solo
  cambie ese archivo.
- Estados: "Enviando…" (botón desactivado), "Éxito / pendiente de revisión" y
  "Error" (incluye 401, error de validación del servidor, fallo de red y
  endpoint inexistente/404). El resultado se anuncia con aria-live="polite".
- Todos los textos en en y es.
- Accesibilidad: operable por teclado, foco visible, nada comunicado solo por
  color, respeta prefers-reduced-motion.

Restricciones:
- NO implementes el endpoint del backend ni toques services/backend/** ni
  ttod.yml. Si el endpoint no existe, trabaja contra el mock.
- No inventes campos del contrato: si falta información, pregúntame.

Tests (mockeando fetch y requireUser):
- Con datos válidos, submitProposal envía el payload exacto del contrato.
- Con campos vacíos, no se llama a fetch y aparecen los errores.
- Se muestran los estados de éxito y de error.
- Sin sesión, el formulario no se renderiza (si es viable como integración).

Al terminar:
- Dime cómo probarlo a mano con y sin sesión, en en y es.
- Redacta el texto del contrato para la descripción del PR.
- Resume, para la defensa oral: la coordinación con el Equipo 5, el caso sin
  sesión y por qué validar en cliente además de en el servidor.
- Redacta un borrador de la sección "Uso de IA" para el PR.
```

---

## Tarea 5 — Fuente, derechos y procedencia

| | |
|---|---|
| **Responsable** | Persona A |
| **Semana** | 2 |
| **Verbo** | keep |
| **Depende de** | T1 (listados de facetas) |
| **Lección** | Unidad 3 (esquemas de colecciones de contenido) |

### Objetivo

Que cada cita muestre visiblemente su titular (`rights.holder`), su licencia (`rights.license`) y su origen (`origin`), no solo el texto. Debe verse en el índice, en las facetas y en el detalle.

### Punto de partida

`WisdomEntry` ya incluye `rights` y `origin`, y `fetchWisdom` ya los trae. El detalle muestra el texto, pero no un bloque de procedencia accesible y consistente. **No hacen falta llamadas nuevas.**

### Qué hay que hacer

1. Crear un componente reutilizable, `src/components/ProvenanceBlock.astro`, que reciba un `WisdomEntry`.
2. Usar HTML semántico: `<dl>`, `<dt>`, `<dd>` para los pares etiqueta–valor.
3. Integrarlo en las tarjetas del índice, en los listados de facetas y en el detalle.
4. Comprobar que se ve bien en `/en/` y `/es/`.
5. Manejar `rights` u `origin` nulos o ausentes, ocultando el bloque o mostrando un texto de reserva, sin romper el diseño.

### Criterios de aceptación

- [ ] Procedencia visible en las tarjetas del índice.
- [ ] Procedencia visible en los listados de sección, etiqueta y nivel.
- [ ] Procedencia en el detalle, en un bloque claramente etiquetado.
- [ ] Funciona en ambos idiomas con la misma fuente de datos.
- [ ] Sin llamadas nuevas al backend ni archivos estáticos nuevos.
- [ ] Los datos ausentes no rompen el diseño.

### Criterios de calidad

- **Un solo componente**, importado en los tres tipos de vista.
- **Documentación:** en el PR, por qué un componente compartido y qué se gana o se pierde.
- **Test (Trophy):** un test de integración del detalle con un fixture real de `WisdomEntry`. Los tests unitarios del componente son opcionales.
- **Accesibilidad:** la Definición de Hecho heredada, con `<dl>`.

### Defensa oral

"Hice un único componente de procedencia que muestra titular, licencia y origen a partir del `WisdomEntry`. Lo usé en índice, facetas y detalle para que la atribución esté siempre visible. Usé HTML semántico y comprobé que los datos ausentes no rompen nada."

### Prompt para Claude Code

```text
Contexto: proyecto TTOD (Astro), módulo de contenido del Equipo 1. Tarea:
mostrar la procedencia de cada cita (titular, licencia y origen) en todas las
vistas de contenido ("wisdom"), en en y es.

Antes de escribir código, explora y resume:
1. services/frontend/src/types/domain.ts: la forma exacta de rights (holder,
   license, ¿más campos?) y de origin en WisdomEntry, y cuáles pueden ser
   null o undefined.
2. Muestras reales del payload de fetchWisdom (fixtures o datos de ejemplo)
   para ver valores reales de rights y origin, incluidos casos incompletos.
3. Dónde se renderizan las citas: tarjetas en
   services/frontend/src/pages/[locale]/wisdom/index.astro, listados en las
   rutas de facetas (sections/tags/levels) y el detalle en [slug].astro. Si
   hay un componente de tarjeta compartido, dímelo.
4. Cómo se traducen las cadenas de la interfaz.
5. Qué framework de tests se usa y si hay fixtures de WisdomEntry.
Después, preséntame un plan (API del componente, variante compacta para
tarjetas frente a completa para el detalle si hace falta, archivos a tocar) y
ESPERA a que lo apruebe.

Requisitos:
- Un único componente reutilizable, src/components/ProvenanceBlock.astro, que
  recibe un WisdomEntry (o solo rights y origin) y muestra titular, licencia y
  origen. Si necesitas una versión compacta para las tarjetas, que sea una
  prop del MISMO componente (p. ej. variant="compact"), no un segundo
  componente.
- HTML semántico: <dl> con <dt>/<dd>. Las etiquetas ("Titular", "Licencia",
  "Origen") traducidas en en y es.
- Si la licencia o el origen tienen una URL en los datos, enlázala con texto
  descriptivo; no inventes URLs.
- Datos ausentes: si falta un campo, omite solo ese par; si faltan todos,
  oculta el bloque o muestra un texto de reserva traducido. Nunca "undefined"
  ni diseño roto.
- Intégralo en las tarjetas del índice, en los listados de las facetas (si
  existen; si no, dime qué añadir) y en el detalle.
- Usa solo los datos que ya trae fetchWisdom: nada de llamadas nuevas.
- Accesibilidad: el bloque tiene un nombre accesible (encabezado o
  aria-label), nada comunicado solo por color, respeta prefers-reduced-motion.

Restricciones:
- No toques services/backend/** ni ttod.yml.
- Cambios mínimos en las páginas, que otras tareas también editan.

Tests:
- Un test de integración del detalle con un fixture real de WisdomEntry que
  compruebe titular, licencia y origen.
- Un caso con rights u origin ausentes que no rompa el render.

Al terminar:
- Dime cómo comprobarlo a mano en las tres vistas y en ambos idiomas.
- Redacta la nota de decisión para el PR (componente compartido frente a
  render en línea, y qué se gana o se pierde).
- Redacta un borrador de la sección "Uso de IA" para el PR.
```

---

## Tarea 6 — Tests unitarios y de componente

| | |
|---|---|
| **Responsables** | Persona A (rutas y `frequencies()`) + Persona B (formulario) |
| **Semana** | 3 (hackathon), aunque conviene ir escribiendo tests con cada tarea |
| **Verbo** | keep |
| **Depende de** | T1 y T4 |
| **Lección** | Unidad 5 — Estrategia de testing (Trophy, no Pyramid) |

### Objetivo

Que las rutas de contenido y el formulario de propuesta tengan al menos un test real cada uno, ejecutándose en el mismo job de CI que los tests de los demás módulos.

### Qué hay que hacer

1. Elegir la capa más barata que dé confianza real para cada objetivo.
2. **Test unitario** de `frequencies()` (función pura): cuenta bien por `section`, `level` y `tags`.
   - La ficha de la T1 dice que `frequencies()` ya se prueba donde se define. **Comprobadlo primero:** si existe el test, completad los casos que falten en lugar de duplicarlo.
3. **Test de componente** del formulario (o de una ruta de contenido): estructura del DOM y validación.
4. Comprobar que ambos corren en CI.

Si en las tareas anteriores ya se hicieron tests, esta tarea consiste en **cerrar huecos**, no en empezar de cero.

### Criterios de aceptación

- [ ] Test unitario de `frequencies()` que pasa, cubriendo `section`, `level` y `tags`.
- [ ] Test de componente del formulario (o de una ruta) que pasa: DOM esperado y validación.
- [ ] Ambos se ejecutan en el job de CI junto a los demás módulos.

### Criterios de calidad

- **Organización:** los tests van junto al código o en la estructura que ya use el proyecto, con nombres claros.
- **Documentación de IA:** qué se generó y qué se verificó a mano.
- **Forma Trophy:** unitarios para la lógica pura, de componente para el render y el estado. Nada de E2E pesados para lo que cubre una capa más barata.
- **Accesibilidad:** el test del formulario comprueba etiquetas y nombres accesibles, y operabilidad por teclado en la medida de lo posible.

### Defensa oral

- Por qué unitario para `frequencies()` (pura, sin efectos secundarios) y de componente para el formulario (render y estado).
- Cómo se integran en CI.
- Cómo sabéis que los tests verifican de verdad. Buena prueba: romper el código a propósito y ver que el test falla.

### Prompt para Claude Code

```text
Contexto: proyecto TTOD (Astro), módulo de contenido del Equipo 1. Tarea:
completar los tests del módulo siguiendo la doctrina "Testing Trophy, no
Pyramid": la capa más barata que dé confianza real, sin E2E pesados para lo
que cubre un test unitario o de componente.

Antes de escribir código, explora y resume:
1. El framework de tests y su configuración (vitest, @astrojs/test,
   testing-library, etc.) y dónde viven los tests actuales.
2. El workflow de CI (p. ej. .github/workflows/): qué job ejecuta los tests
   del frontend y cómo se incluyen los archivos nuevos.
3. Qué tests existen YA para: frequencies() en
   services/frontend/src/content/wisdom.ts, las rutas de contenido
   (index, [slug], sections/tags/levels), EmptyState, Breadcrumbs,
   ProvenanceBlock y el formulario de propuesta.
4. Qué casos importantes NO están cubiertos.
Después, preséntame un plan con la lista de tests a añadir, la capa de cada
uno (unitario o de componente/integración) y por qué. ESPERA a que lo apruebe.

Requisitos:
- frequencies(): si ya tiene test, NO lo dupliques; añade solo los casos que
  falten. Casos mínimos: cuenta por 'section', por 'level' y por 'tags'
  (una entrada con varias etiquetas cuenta en cada una), array vacío y
  entradas con valores repetidos.
- Formulario de propuesta (test de componente): renderiza <form> con cada
  campo y su <label>; con campos vacíos muestra errores enlazados con
  aria-describedby y NO llama a fetch (mockeado); con datos válidos llama a
  submitProposal/fetch con el payload del contrato; muestra los estados de
  éxito y de error. Mockea requireUser y fetch.
- Si hay tiempo y no existe ya: un test de integración de una ruta de faceta
  que compruebe que solo aparecen las entradas filtradas.
- Tests legibles: nombres que describen el comportamiento, fixtures
  realistas de WisdomEntry y nada de probar detalles internos de
  implementación.
- Comprueba que los tests nuevos se ejecutan en el job de CI existente. Si
  hay que tocar la configuración de CI, explícame el cambio antes de hacerlo.

Restricciones:
- No toques services/backend/** ni ttod.yml.
- No cambies código de producción para "hacer pasar" un test. Si un test
  revela un bug, avísame y proponme el arreglo por separado.

Al terminar:
- Ejecuta la suite y enséñame el resultado.
- Para cada test nuevo, dime qué cambio en el código lo haría fallar (para
  demostrar que prueba algo real).
- Resume, para la defensa oral, por qué cada test está en la capa elegida
  según la doctrina Trophy.
- Redacta un borrador de la sección "Uso de IA" para el PR.
```

---

## Tarea 7 — Abrir un PR en un módulo que no es nuestro

| | |
|---|---|
| **Responsable** | Persona A |
| **Semana** | 3 (hackathon). Se puede ir explorando antes |
| **Verbo** | contribute |
| **Depende de** | Que el otro módulo tenga código (ya hay código base en todos) |

### Qué es

Salir de `src/content` y `src/pages/[locale]/wisdom` para enviar **un arreglo o una mejora pequeña y real** a un módulo de otro equipo: Graph (Equipo 2), Oracle (Equipo 3), PWA (Equipo 4) o Accounts (Equipo 5).

### Qué exige

- **No vale un commit de una errata.** Hay que leer y modificar código que no escribisteis vosotros.
- Se evalúa como **evidencia de proceso**, no como crédito extra.
- Según la ficha, es la única tarea que una IA no puede resolver de una sola vez. El valor está en entender un sistema ajeno.

### Cómo abordarla

1. Durante las semanas 1 y 2, apuntad cosas mejorables que veáis en otros módulos al integrar los vuestros. Son buenos candidatos los puntos donde nuestro trabajo toca el suyo:
   - accesibilidad de un componente del grafo;
   - un texto sin traducir en `es` en otro módulo;
   - un estado de error que falta.
2. Leed el `ASSIGNMENT.md` de ese equipo para no pisar una tarea que ya tienen asignada.
3. Hablad con el equipo dueño antes de abrir el PR: qué queréis cambiar y por qué.
4. PR pequeño y enfocado, con una descripción clara (problema, cambio, cómo probarlo) y la sección de uso de IA.
5. Responded a la revisión que os hagan e iterad.

Consultad la explicación común en `docs/public/teaching/tasks.md#the-three-recurring-tasks` y la guía de contribución (`/guides/contributing/`).

---

## Tarea 8 — Revisar formalmente un PR de otro módulo

| | |
|---|---|
| **Responsable** | Persona B |
| **Semana** | 3 (hackathon) |
| **Verbo** | contribute |
| **Depende de** | Que otro equipo abra un PR. Pactad una revisión cruzada pronto |

### Qué es

Elegir un PR de otro equipo y evaluarlo **estrictamente contra el `ASSIGNMENT.md` de ese equipo**, no contra vuestro gusto ni con criterios generales de estilo.

### Qué exige

Comprobar si su implementación cumple:

- los **resultados de aprendizaje** de su ficha;
- las **restricciones** (por ejemplo, qué archivos no pueden tocar);
- los **criterios de aceptación**.

Esto obliga a entender los límites de sistemas que no habéis construido y cómo encaja vuestro trabajo de contenido e i18n con ellos.

### Cómo abordarla

1. Leed la ficha completa de la tarea del otro equipo **antes** de mirar el código.
2. Montad una tabla con cada criterio de aceptación y su veredicto (cumple / no cumple / parcial), con evidencia: línea de código, captura o comando.
3. Comprobad las restricciones y la Definición de Hecho de accesibilidad.
4. Probad el PR en local si es posible.
5. Escribid comentarios concretos y constructivos, citando el criterio de su ficha en cada uno.
6. Recordad la regla de la Unidad 6: la IA puede ayudar a comentar, pero **la decisión y la aprobación son humanas y vuestras**.

Consultad `docs/public/teaching/tasks.md#the-three-recurring-tasks` y la guía `/guides/reviewing-cohort-prs/`.

---

## Tarea 9 — Documentar una decisión de diseño real

| | |
|---|---|
| **Responsables** | Persona A + Persona B |
| **Semana** | 3 (hackathon), con notas desde la semana 1 |
| **Verbo** | question |
| **Depende de** | Que la decisión ya exista en el código |

### Qué es

Elegir **una** decisión arquitectónica concreta que hayáis tomado en el módulo y preparar su defensa, incluida la **alternativa que descartasteis** y por qué.

### Candidatos naturales

- **Taxonomía de facetas** (T1/T2), de Persona A. Por ejemplo:
  - rutas separadas `/sections/`, `/tags/`, `/levels/` frente a una única ruta con parámetros de consulta;
  - una jerarquía de breadcrumbs más plana frente a una más profunda.
- **Política de fallback** (T3/T4), de Persona B. Por ejemplo:
  - qué pasa cuando no hay entradas en un idioma: estado vacío frente a mostrar las del otro idioma;
  - `try/catch` por ruta frente a `error.astro`;
  - estado "no encontrado" en el componente frente a una 404 del servidor.

### Qué exige

- La decisión no puede ser accidental. Tiene que venir de haber evaluado una alternativa concreta y haberla rechazado por una razón defendible: mantenibilidad, experiencia de usuario o integridad del sistema.
- Tiene que estar escrita con claridad, de forma que se pueda defender bajo presión.

### Cómo abordarla

1. Desde la semana 1, apuntad cada vez que elijáis entre dos opciones: fecha, opciones, qué elegisteis y por qué.
2. En la semana 3, elegid la decisión más sólida y redactadla con esta estructura:
   - contexto;
   - opciones consideradas;
   - decisión;
   - consecuencias (lo que se gana y lo que se pierde);
   - evidencia en el código (archivos y líneas).
3. Ensayad la defensa el uno con el otro, intentando rebatiros mutuamente.

Consultad `docs/public/teaching/tasks.md#the-three-recurring-tasks`.

---

## Checklist final antes de la defensa

**Funcionalidad**

- [ ] Las tres rutas de facetas funcionan en `en` y `es`.
- [ ] Breadcrumbs en índice, facetas y detalle.
- [ ] Estados vacío, "no encontrado" y de error, sin páginas en blanco.
- [ ] Formulario de propuesta con control de sesión, validación y estados.
- [ ] Procedencia visible en índice, facetas y detalle.

**Calidad**

- [ ] `frequencies()` reutilizada, sin contadores a mano.
- [ ] Componentes compartidos (`EmptyState`, `Breadcrumbs`, `ProvenanceBlock`) sin duplicación.
- [ ] Nada tocado en `services/backend/**` ni `ttod.yml`.
- [ ] Tests en CI y en verde.
- [ ] Accesibilidad revisada con teclado y lector de pantalla en cada vista.
- [ ] Sección "Uso de IA" en cada PR.

**Tareas transversales**

- [ ] Contrato con el Equipo 5 documentado (sección 4 y PR de la T4).
- [ ] T7: PR abierto en otro módulo.
- [ ] T8: revisión hecha contra la ficha del otro equipo.
- [ ] T9: decisión de diseño redactada.

**Defensa oral (los dos debéis poder explicarlo)**

- [ ] Dónde se llama a `frequencies()` y por qué se filtra sobre el payload existente.
- [ ] Cómo se obtiene y valida el idioma.
- [ ] Por qué hay componentes compartidos y cómo manejan las distintas profundidades.
- [ ] La decisión sobre el manejo de errores y el código HTTP del "no encontrado".
- [ ] Cómo se coordinó el contrato con el Equipo 5 y cómo se trata el caso sin sesión.
- [ ] Por qué cada test está en la capa en la que está.
- [ ] La decisión de diseño de la T9 y la alternativa descartada.
