# Convocatoria — Defensa oral TTOD («diff review»)

**Audience:** borrador para campus virtual (alumnado) + notas de instructor.  
**No publicar** bajo `docs/public/` hasta cerrar fecha/enlace y política de notas.  
**Rúbrica fuente:** [`PHASE-V-FEII-COHORT-COLLABORATION-AND-ASSESSMENT.md`](../PHASE-V-FEII-COHORT-COLLABORATION-AND-ASSESSMENT.md) §6.

---

## Nota de instructor (no pegar en campus)

- **Precondición de la sesión:** todas las PRs del sprint deben estar **ya mergeadas** en `main` antes de la defensa. La sesión evalúa comprensión sobre el producto integrado, no sobre ramas abiertas ni demos a medias. Si alguna PR sigue abierta, no abrir la convocatoria o retrasar el slot del equipo afectado.
- Scorecard PR (§5) y defensa oral (§6) se puntúan por separado; el merge no sustituye la defensa.
- Formato acordado aquí: **15 min por equipo + turno de preguntas** (ajuste respecto al borrador §6 que proponía ~15 min por estudiante).

---

## Texto para el campus virtual

**Asignatura:** Front-End II · Web Atelier (UDIT)  
**Actividad:** Defensa oral del trabajo desarrollado en The Tao of Development (TTOD Oráculo)  
**Formato:** Sesión síncrona por equipos · **15 minutos de exposición + turno de preguntas**  
**Fecha / hora / enlace:** *[completar]*  
**Asistencia:** Obligatoria para todos los miembros del equipo

### 1. Propósito

Tras el sprint de desarrollo colaborativo, esta defensa no es una demo de producto acabado. Es la comprobación de que **entendéis el código que habéis entregado**, la **arquitectura de la aplicación** en la que se inserta vuestro módulo, y el **uso responsable de la IA** como herramienta de apoyo — no como autoría opaca.

En línea con los objetivos de Web Atelier y de la Entrega 1 / parcial de proceso:

- uso **declarativo** del sistema (saber qué hace cada capa y por qué);
- **defensa del proceso** (cómo llegasteis a las decisiones, no solo el resultado);
- **comprensión del código** (poder explicar y modificar lo entregado).

Un módulo que «pasa CI» o una interfaz pulida **no sustituyen** esta evidencia.

**Estado del repositorio en el día de la defensa:** el trabajo evaluable del sprint estará **integrado en `main`** (PRs mergeadas). Preparad la exposición sobre ese estado integrado, no sobre ramas locales o PRs pendientes.

### 2. Qué se evalúa

| Dimensión | Qué debéis demostrar |
| --- | --- |
| **Profundidad en vuestro módulo** | Recorrer un *diff* real (PR mergeada o conjunto de cambios en `main`), explicar **una decisión de diseño concreta** y al menos **una alternativa** que descartasteis. |
| **Fluidez de sistema (arquitectura)** | Situar vuestro trabajo en el conjunto: dónde viven el renderizado, el estado, la confianza/auth, el offline/PWA y el Oráculo — **también fuera** de vuestro seam. |
| **Uso de IA** | Mostrar evidencia de proceso (AI Review Log / declaraciones en PRs): qué generó la IA, qué verificasteis vosotros, y **al menos una sugerencia rechazada o revisada** con motivo. |
| **Preguntas del profesorado** | Responder a preguntas sobre vuestro código y, en su caso, sobre un módulo que **no** os pertenecía — prueba de amplitud, no solo de especialización. |
| **Preguntas a compañeros** | Durante el turno de otros equipos, **preguntar con criterio** suma valoración: muestra que escucháis, que entendéis la arquitectura compartida y que podéis dialogar sobre código ajeno. Preguntas vagas, de relleno o que solo demuestren presencia no puntúan. |
| **Recuperación bajo duda** | Si no sabéis algo, razonar en voz alta («miraría X / comprobaría Y») vale más que improvisar. |

### 3. Formato de la sesión (15 min + preguntas)

**Exposición (~15 min, el equipo completo)**

1. **Contexto del seam** (1–2 min): qué persona/recorrido de usuario cubre vuestro módulo y qué contrato respetáis.
2. **Arquitectura** (3–4 min): situad vuestro módulo en el sistema TTOD (diagrama `ttod-feii-architecture` o esquema propio dibujado). Dejad claro qué ocurre *antes* y *después* de vuestro código.
3. **Diff walkthrough** (5–6 min): un cambio real ya en `main`, con decisión de diseño + alternativa. Preferid profundidad a recorrer todos los PRs.
4. **Proceso e IA** (2–3 min): log / historial; qué aceptasteis, qué rechazasteis, cómo lo verificasteis (tests, a11y, contrato).

**Turno de preguntas** (después de los 15 min)

1. Preguntas del profesorado (pueden dirigirse a cualquier miembro del equipo).
2. Preguntas del resto de la cohorte. **Formular buenas preguntas a otros equipos suma valoración** para quien pregunta; responderlas forma parte de la defensa del equipo que expone.

### 4. Preparación mínima (checklist)

Antes de la sesión, cada equipo debe tener listo:

- [ ] Capacidad de trabajar sobre el producto en `main` (PRs del sprint ya mergeadas).
- [ ] Un *diff* concreto (commit/PR mergeada) para recorrer en pantalla.
- [ ] Capacidad de explicar, en palabras propias, el flujo de datos / render / errores de su módulo.
- [ ] Una decisión de diseño documentada (tarea de proceso del backlog) + alternativa considerada.
- [ ] AI Review Log (o equivalente en las PRs) **honesto** y localizable.
- [ ] Visión básica de la arquitectura global (no hace falta memorizar cada archivo ajeno; sí saber **dónde** viven rendering, estado, trust y offline).
- [ ] Al menos una pregunta preparada para otro equipo cuyo seam toca el vuestro (integración, contrato, accesibilidad, offline, auth, etc.).

**No hace falta** una presentación larga ni una demo de caja negra. Si enseñáis la app, que sea para anclar una explicación técnica, no para «enseñar pantallas».

### 5. Criterios de calidad (qué se premia / qué no)

**Se valora**

- Explicar *por qué* (límites de archivo, contrato, accesibilidad, política de caché, sesión vs token, etc.).
- Señalar límites y deudas conocidas con claridad.
- Distinguir andamiaje de IA de **comprensión humana** (modificar, probar, rechazar).
- Conectar vuestro seam con el resto del producto.
- Preguntas a compañeros que demuestren comprensión del sistema y escucha activa.

**No basta**

- Leer el README o pegar una explicación generada sin poder defenderla.
- «Lo hizo el copiloto / el agente» sin verificación ni criterio.
- Conocer solo «vuestra carpeta» y desconocer por completo el sistema.
- Preguntas genéricas («¿qué os ha costado más?») sin anclaje técnico.

### 6. Relación con la investigación (recordatorio breve)

La defensa forma parte de la **evaluación ordinaria** de la asignatura. La posible participación en el estudio asociado a TTOD (uso secundario seudonimizado de trazas de proceso) es **voluntaria**, independiente de la nota, y no cambia lo que debéis preparar para esta convocatoria.

### 7. Organización práctica

- Orden de equipos: *[completar]*
- Canal / sala: *[completar]*
- Materiales de apoyo recomendados: diagrama de arquitectura del curso, PRs mergeadas, AI Review Log de la Unidad 6.
- Si un miembro no puede asistir por causa justificada: avisar con antelación; la defensa del equipo se mantiene y se acordará recuperación individual si procede.

---

### Mensaje corto (versión anuncio)

> **Convocatoria — Defensa oral TTOD (diff review)**  
> Cada equipo dispone de **15 minutos** para demostrar comprensión del código desarrollado y del uso de IA, más un **turno de preguntas**. El código evaluable estará **ya mergeado en `main`**. No es una demo de interfaz: debéis situar vuestro módulo en la **arquitectura** de la aplicación, recorrer un *diff* real con decisión de diseño y alternativa, y evidenciar el proceso (incluido qué aceptasteis o rechazasteis de la IA). **Preguntar con criterio a los compañeros durante sus defensas suma valoración.** Fecha/hora/enlace: *[completar]*.
