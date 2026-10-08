<!--
Checklist frente al comunicado del Comité de Ética de Investigación.
Strand B · TTOD / Front-End II · 2026-09-26.
-->

# Checklist — requisitos del Comité de Ética (Strand B)

Mapa de lo que el comunicado pide frente a lo que **ya hay** en el repositorio y lo que
**falta o está incompleto** para la remisión.

| # | Requisito del comunicado | Estado | Documento canónico (ES) |
| - | ------------------------ | ------ | ----------------------- |
| 1 | **Protocolo de investigación completo** | **Parcial → consolidado** | [`PROTOCOLO-INVESTIGACION-COMPLETO-ES.md`](PROTOCOLO-INVESTIGACION-COMPLETO-ES.md) (síntesis para remisión). Diseño detallado también en [`../STRAND-B-PEDAGOGICAL-DESIGN.md`](../STRAND-B-PEDAGOGICAL-DESIGN.md) |
| 2 | **Formulario de consentimiento informado** | **Listo (plantilla)** | [`PARTICIPANT-CONSENT-FORM-ES.md`](PARTICIPANT-CONSENT-FORM-ES.md) + hoja [`PARTICIPANT-INFORMATION-SHEET-ES.md`](PARTICIPANT-INFORMATION-SHEET-ES.md). Firmados: fuera de git — [`SIGNED-CONSENTS-CUSTODY.md`](SIGNED-CONSENTS-CUSTODY.md) |
| 3 | **Instrumentos de recolección de datos** | **Faltaba como anexo formal** → creado | [`INSTRUMENTOS-RECOLECCION-DATOS-ES.md`](INSTRUMENTOS-RECOLECCION-DATOS-ES.md). *No* hay cuestionario ni entrevista en el diseño mínimo |
| 4 | **Autorizaciones institucionales** | **Incompleto** | [`AUTORIZACIONES-INSTITUCIONALES-ES.md`](AUTORIZACIONES-INSTITUCIONALES-ES.md) — checklist; falta adjuntar acta/correo departamental firmado y, si aplica, DPO |
| 5 | **Plan de manejo de datos** | **Parcial** (solo minimización) → creado plan | [`PLAN-MANEJO-DATOS-ES.md`](PLAN-MANEJO-DATOS-ES.md); complemento [`DATA-MINIMIZATION-STATEMENT.md`](DATA-MINIMIZATION-STATEMENT.md) |
| 6 | **Otra documentación relevante** | **Parcial** | Ver § abajo |

---

## Qué falta todavía (acción humana / institucional)

1. **n del grupo:** **8** (*README* *Development Team*, excluido PI). **Tasa de consentimiento B** aún por registrar en custodia offline.
2. **Autorización departamental firmada** (correo/acta) — no basta el brief interno
   [`../DEPARTMENT-DECISION-BRIEF.md`](../DEPARTMENT-DECISION-BRIEF.md).
3. **Contacto del DPO / delegado de protección de datos** en hoja de información (institucional: `dpd@udit.es`).
4. **Custodio independiente** nombrado (si el comité lo exige para rol docente–investigador).
5. **CV del PI** / ficha del proyecto en el formato que pida el comité (si lo piden).
6. **Export PDF** del paquete con portada institucional (el repo guarda Markdown; la remisión
   suele ser PDF).
7. Si el comité exige **cuestionarios/entrevistas**: hoy están **desactivados**; habría que
   redactarlos y ampliar consentimiento (ítems D/E) — no están en el diseño mínimo.

---

## Otra documentación relevante (punto 6)

| Documento | ¿Incluir en remisión? |
| --------- | --------------------- |
| [`ETHICS-COMMITTEE-SUBMISSION-ES.md`](ETHICS-COMMITTEE-SUBMISSION-ES.md) | Sí — carta / solicitud |
| [`AUTORIA-LICENCIA-COHORTE-ES.md`](AUTORIA-LICENCIA-COHORTE-ES.md) | Sí — autoría de producto + MIT (ítem H); distinto del corpus investigador |
| [`DECLARACION-AUTORIA-ASISTIDA-POR-IA-ES.md`](DECLARACION-AUTORIA-ASISTIDA-POR-IA-ES.md) | Sí — transparencia del PI (no confundir con I2 del alumnado) |
| [`../STRAND-A-PHILOSOPHICAL-PARKED.md`](../STRAND-A-PHILOSOPHICAL-PARKED.md) | Sí, breve — declara exclusión |
| [`../DEPARTMENT-DECISION-BRIEF.md`](../DEPARTMENT-DECISION-BRIEF.md) | Sí como anexo de encuadre pedagógico; **más** la autorización firmada |
| Extracto guía docente / encargo Entrega 1 | Sí — fuera o dentro según derechos |
| Bibliografía / columna metodológica | Dentro del protocolo § referencias |
| Profield inheritance / claim registry | **No** — interno del estudio |
| Firmas de consentimiento escaneadas | **No en git**; sí en el expediente del comité según su vía |

---

## Paquete mínimo recomendado para enviar

1. Formulario CEI Word — `FORMULARIO-SOLICITUD-CEI-UDIT-RELLENO.docx`  
2. Anexos blended (PDF) — `PAQUETE-REMISION-CEI-UDIT-ES.pdf`  
3. Adjuntos firmados fuera de git (A1; consentimientos según vía)

Fuente LaTeX del blend: `latex/PAQUETE-REMISION-CEI-UDIT-ES.tex` (`make remision`).
