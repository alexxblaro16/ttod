---
title: Contribuir
eyebrow: Gobernanza antes que comodidad
description: Cómo abrir una PR como colaborador, cómo la procesa quien revisa, y las expectativas públicas de contribución detrás de ambas.
permalink: /es/guides/contributing/
lang: es
---

# Haz viajar la evidencia con el cambio

Una contribución debería identificar qué cambió, por qué corresponde, cómo se verificó y qué
incertidumbre permanece. Esta página cubre la mecánica —abrir una PR, qué le pasa después, y cómo
la procesa quien revisa— antes de los principios de gobernanza sobre los que descansan ambas.

## Abrir una PR (trabajo de módulo)

1. Crea una rama desde la base docente actual:
   `git checkout -b <seam>-task<N>-<tema-corto>` — p. ej. `content-task2-browse-routes` o
   `accounts-task2-personal-library`. La parte `<seam>-task<N>` (`content`, `graph`, `oracle`,
   `pwa` o `accounts`, más el número de tarea) es la que usa el bot de revisión para cargar los
   criterios de esa ficha. Prefiere esa forma; algunos alias cortos (p. ej.
   `task/2-personal-library`) se rescatan en el constructor del prompt, pero fuera del patrón
   documentado la revisión puede ser solo genérica.
2. Haz el cambio dentro de los archivos de tu propio módulo — los criterios de aceptación viven en
   `/es/teaching/tasks/<seam>-task<N>/` en este sitio (no hay un `ASSIGNMENT.md` dentro del código
   de la app); esa página enlaza a su fuente en GitHub.
3. Antes de subir la rama, ejecuta las mismas comprobaciones que correrá la CI:
   `npm run check && npm run build` en `services/frontend` (o el equivalente para un cambio de
   backend).
4. Abre la PR. La plantilla del repositorio se rellena automáticamente — refleja directamente la
   rúbrica de evaluación: adherencia al contrato, criterios de aceptación, cobertura de pruebas,
   la Definición de Terminado de accesibilidad, y el Registro de Revisión de IA (la propia
   plantilla de la Unidad 6 — qué se hizo con ayuda de IA, qué verificaste tú mismo).
5. La comprobación obligatoria `typecheck-and-build` debe pasar y se exige al menos una revisión
   aprobatoria antes de fusionar — ambas se aplican automáticamente, no por convención.
6. Una PR pequeña que se entrega por etapas se defiende mejor que una PR grande que llega de
   golpe — el [modelo docente]({{ '/es/teaching/' | relative_url }}) explica por qué eso es parte
   del diseño, no solo una preferencia de estilo.

**Las contribuciones entre módulos también cuentan.** Al menos una PR hacia un módulo que no es el
tuyo, y al menos una revisión formal de una PR fuera de tu propio módulo, forman parte de la
tarea — ver [tareas y backlog]({{ '/es/teaching/assignments/' | relative_url }}) para saber por
qué.

## Proponer una cita (contribución de contenido)

Está cubierto en detalle en [tareas y backlog]({{ '/es/teaching/assignments/' | relative_url }}) —
la versión corta: envíala mediante el formulario de propuesta (o `cli.py proposal create`
directamente) con sesión iniciada, una persona revisora la lee y puede pedir cambios, y solo una
segunda aprobación explícita sobre el diff canónico calculado la publica de verdad. Dos
aprobaciones separadas, no una — la primera aprueba la idea, la segunda aprueba el cambio exacto.

<figure class="diagram-teaser">
  <a class="diagram-teaser-link" href="{{ '/assets/diagrams/ttod-proposal-review.html' | relative_url }}">
    <img src="{{ '/assets/diagrams/ttod-proposal-review.png' | relative_url }}" alt="Diagrama de flujo: una persona colaboradora envía una propuesta, se abre una PR, quien revisa la aprueba, un bot calcula y empuja el diff canónico lo que despeja esa aprobación, quien revisa aprueba de nuevo sobre el diff exacto, y solo entonces la PR se fusiona y ttod.yml se actualiza." loading="lazy">
  </a>
  <figcaption><a href="{{ '/assets/diagrams/ttod-proposal-review.html' | relative_url }}">Abrir el diagrama interactivo del pipeline de revisión ↗</a> — el mismo mecanismo de doble aprobación que ejecuta este repositorio, no una versión simplificada. (Interfaz en inglés.)</figcaption>
</figure>

## Para quien revisa

- `make review-queue` lista las PR abiertas que esperan tu revisión, las PR de propuestas en
  particular, y todo lo demás abierto — de solo lectura, nunca aprueba ni fusiona en tu nombre.
- Revisa contra los criterios de aceptación de la [ficha de la tarea]({{ '/es/teaching/tasks/' | relative_url }})
  y la lista de la plantilla de PR, no contra una impresión genérica de calidad de código. El bot
  etiqueta hallazgos como `MUST FIX:` o `NIT:` — pide cambios solo sobre MUST FIX.
- Una PR sin su entrada del Registro de Revisión de IA está incompleta, no simplemente
  poco documentada.
- Para una PR de propuesta de cita en particular: tu aprobación sobre la propuesta *original* no
  es el mismo evento que tu aprobación sobre el *diff calculado* que el bot empuja después — la
  protección de rama despeja intencionadamente la primera aprobación para que mires la segunda.
  Eso no es un fallo que rodear.

## Contenido canónico

- Nunca añadas de forma directa a la colección YAML canónica.
- Propón material nuevo por el camino gobernado de propuestas.
- Conserva identificadores estables; marca el material sustituido como obsoleto en lugar de borrarlo.
- Usa la taxonomía de etiquetas definida, el modelo de origen, la política de idioma y los campos de derechos.
- No cites propuestas pendientes como entradas aceptadas.

## Trabajo de front-end

- Conserva la localización, el HTML semántico, el uso de teclado y los estados explícitos de carga, vacío, error y recuperación.
- Mantén las islas de marco acotadas por una razón para hidratar.
- Prueba el riesgo en la capa más barata que dé confianza útil.
- Mide el coste de paquete o de tiempo de ejecución antes de afirmar una optimización.

## Investigación y publicación

- Separa la racionalidad de diseño de la evidencia de aprendizaje.
- Usa fuentes autorizadas para los requisitos legales o institucionales vigentes.
- No expongas rutas locales, anfitriones internos, coordenadas de red, nombres de infraestructura privada, secretos ni utillaje privado del estudio.
- Usa referencias relativas al repositorio en los artefactos públicos y la identidad de estudio `@crea-comm.net`.
