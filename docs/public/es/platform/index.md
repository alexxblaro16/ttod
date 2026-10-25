---
title: Áreas de producto
eyebrow: La referencia implementada
description: Las áreas visibles y los límites de front-end en la referencia docente de TTOD.
permalink: /es/platform/
lang: es
---

# Un producto, varios límites enseñables

La referencia del profesorado se puede ejecutar de extremo a extremo en local. Sus áreas no son demostraciones separadas: comparten localización, contratos de contenido, límites de API, estados accesibles en el navegador y la misma fuente de citas, sujeta a gobernanza humana.

| Área | Propósito visible para quien usa | Idea de front-end que se hace observable |
| --- | --- | --- |
| Bienvenida | entrar en inglés o en español | enrutado localizado e idioma del documento |
| Cita | inspeccionar una entrada gobernada | datos tipados, procedencia, derechos y presentación semántica |
| Sabiduría | recorrer la colección | arquitectura de información, filtros y estados vacíos |
| Documentación | aprender el sistema en contexto | colecciones de contenido y navegación editorial |
| Grafo | explorar entradas relacionadas | una isla Svelte hidratada con estado textual accesible |
| Oracle | preguntar y recibir una respuesta en flujo | una isla React, estado en streaming, fuentes y recuperación |
| Operación local | arrancar y observar el conjunto | el límite navegador/servicio, no un temario de operaciones |
| Cuenta y biblioteca | iniciar sesión, guardar citas, proponer nuevas | sesiones verificadas en servidor, una API con token de acceso, y el camino revisado que sigue una propuesta hasta la colección gobernada |
| Pruebas | situar la evidencia en capas útiles | razonamiento unitario, de componente, de contrato, de ruta y de accesibilidad |

## Arquitectura a escala docente

```text
localized route
  → Astro document and content contract
  → bounded Svelte or React island
  → HTTP or streamed request
  → application and retrieval contracts
  → governed quote snapshot
  → accessible browser state
  → test at the cheapest useful layer
```

Astro posee el documento y las rutas orientadas al contenido. Las islas interactivas se usan donde el estado local o el streaming lo justifican. El backend se explica solo lo bastante para trazar la petición y el límite de confianza; el énfasis docente permanece en la arquitectura front-end.

La biblioteca personal queda deliberadamente fuera del corpus gobernado: Redis almacena un hash
por usuario de `quoteId → savedAt`, mientras el backend vuelve a validar cada referencia contra
la instantánea pública y activa antes de devolverla. Así los datos de preferencias pueden cambiar
sin permitir que modifiquen `ttod.yml`.

<figure class="diagram-teaser">
  <a class="diagram-teaser-link" href="{{ '/assets/diagrams/ttod-system-overview.html' | relative_url }}">
    <img src="{{ '/assets/diagrams/ttod-system-overview.png' | relative_url }}" alt="Diagrama del sistema: agentes IDE y ttod-bridge proponen cambios, una persona revisora acepta hacia el almacén canónico ttod.yml, el entorno de solo lectura de Astro, la API Oracle y el servidor MCP dentro de la red Docker Compose, y Ollama mostrado dos veces: el contenedor propio de la aplicación (el valor por defecto de make up) y un Ollama personal tomado manualmente del host." loading="lazy">
  </a>
  <figcaption><a href="{{ '/assets/diagrams/ttod-system-overview.html' | relative_url }}">Abrir el diagrama interactivo del sistema ↗</a> — el mismo recorrido de arriba, como mapa completo de componentes con límites de confianza y vistas guiadas. (Interfaz en inglés.)</figcaption>
</figure>

## Madurez honesta

La referencia rica demuestra contenido localizado, exploración del grafo y un Oracle en flujo. La operación en el navegador, el comportamiento sin conexión y la superficie de pruebas todavía no constituyen una implementación completa lista para el alumnado. Una futura base docente mantendrá cada área principal a profundidad de hello world; esa reducción está prevista, no concluida.

En el [curso FE II](https://ruvebal.github.io/web-atelier-udit/tracks/feii/), esa base es la **Entrega 1** y el producto que se defiende en el parcial de las Unidades 1–7. Consulta el [modelo docente]({{ '/es/teaching/' | relative_url }}).
