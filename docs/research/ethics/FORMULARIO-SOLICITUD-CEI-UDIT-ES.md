<!--
Formulario de solicitud de evaluación ética — CEI UDIT.
Rellenado a partir del paquete Strand B (2026-09-26).
Copiar al formato institucional (Word/PDF) del comité.
Campos entre [corchetes] requieren confirmación humana.
Word relleno (plantilla CEI UDIT): [`FORMULARIO-SOLICITUD-CEI-UDIT-RELLENO.docx`](FORMULARIO-SOLICITUD-CEI-UDIT-RELLENO.docx)
Regenerar: `python3 docs/research/ethics/scripts/fill_cei_formulario.py`
-->

# FORMULARIO DE SOLICITUD DE EVALUACIÓN ÉTICA

**Comité de Ética en Investigación (CEI)** — Universidad de Diseño, Innovación y Tecnología (UDIT)

| Campo | Valor |
| ----- | ----- |
| Fecha de presentación | 26 septiembre 2026 |
| Código de proyecto (si aplica) | **TTOD** (acrónimo interno: `TTOD-Strand-B-FEII-2026-27`) |

> Nota: si el formulario institucional mostró «TTDO», el acrónimo correcto del proyecto es **TTOD** (*The Tao of Development*).

---

## 1. INFORMACIÓN DEL SOLICITANTE

| Campo | Valor |
| ----- | ----- |
| Nombre completo | Rubén Vega Balbás |
| Cargo o afiliación en UDIT | Profesor Adjunto; Investigador grupo ECSIT |
| Departamento o Facultad | Área de Tecnología |
| Correo electrónico institucional | ruben.vega@udit.es |
| Teléfono de contacto | 659 340 115 |

---

## 2. INFORMACIÓN DEL PROYECTO DE INVESTIGACIÓN

**Título del proyecto:**
The Tao of Development (TTOD) — investigación pedagógica asociada a la asignatura Front-End II.

**Título del estudio:**
Aprendizaje haciendo: participación como desarrollador/a en una aplicación real asistida por IA agentica, en grupo, como actividad formativa.

**Investigador/a principal (si es distinto del solicitante):**
No aplica — el solicitante es el investigador principal (PI).

**Otros investigadores involucrados:**
Ninguno en esta versión del protocolo. (Si se incorporara co-investigación metodológica sobre corpus seudonimizado, se notificará al CEI.)

| Nombre | Cargo |
| ------ | ----- |
| — | — |

### Resumen del estudio (máx. 250 palabras)

Se solicita evaluación ética de un **estudio de caso educativo / investigación basada en diseño**, acotado a Front-End II (curso 2026–27). El alumnado participa como desarrolladores en un producto real (plataforma TTOD Oráculo), con asistencia de IA agentica, trabajo en grupo, revisiones por *pull request* y defensa oral. La actividad docente fue autorizada pedagógicamente por el departamento con antelación; la **participación en investigación** (uso secundario seudonimizado de artefactos de proceso) es **voluntaria** e independiente de la calificación.

**Objetivo:** describir *cómo se aprende haciendo* en este entorno y qué principios de diseño pedagógico se desprenden — **no** demostrar causalmente que la IA «mejora el aprendizaje», ni estimar tamaños de efecto poblacionales.

**Metodología:** caso único acotado, cualitativo dominante, con datos ricos de proceso de programación (commits/PRs, declaraciones de uso de IA, notas estructuradas de defensa), seudonimizados tras consentimiento. Sin cuestionarios ni entrevistas en el diseño mínimo. El análisis investigador comienza tras dictamen ético, consentimiento válido y cierre de las calificaciones relevantes.

**Relevancia:** contribuye a la educación informática post-introductoria con GenAI (laguna frente a estudios centrados en CS1) y documenta un diseño de studio / *learning-by-doing* transferible a grupos similares. Una línea filosófica paralela (Strand A) está aparada y **no** usa datos de estudiantes ni forma parte de esta solicitud.

*(≈ 240 palabras)*

---

## 3. DETALLES SOBRE LOS PARTICIPANTES HUMANOS

**¿El estudio implica la participación de seres humanos?**
☑ **Sí**
☐ No

**Número estimado de participantes:**
**8** estudiantes-desarrolladores del grupo TTOD (Front-End II / entrega de producto), auto-listados en el `README` del repositorio (excluido el PI/docente). El corpus investigador incluirá solo a quienes otorguen consentimiento B (**n_consent ≤ 8**). Algunos identificadores GitHub faltan en el listado público; no se usan como dato de análisis.

**Criterios de inclusión:**
Estudiantes matriculados en Front-End II que participan en la entrega del grupo TTOD y otorgan consentimiento informado para el uso investigador secundario seudonimizado de artefactos de proceso (ítem B).

**Criterios de exclusión:**
Quienes no consienten el uso investigador; menores de edad o situaciones de especial vulnerabilidad sin salvaguarda adicional institucional aprobada; artefactos de compañeros no consentidos.

**Descripción de los procedimientos en los que participarán los sujetos:**
No se introducen entrevistas, cuestionarios ni pruebas médicas. Los sujetos realizan la **actividad docente ordinaria** (desarrollo del producto, PRs, declaración de uso de IA, defensa oral). El procedimiento investigador consiste en el **uso secundario seudonimizado** de esas trazas de proceso ya generadas para evaluación, solo tras consentimiento y dictamen del CEI. Instrumentos activos: I1 historial commits/PRs; I2 declaración de IA; I3 notas estructuradas de defensa (sin audio/vídeo); I4 extractos de código solo con consentimiento de difusión. Ver anexo `INSTRUMENTOS-RECOLECCION-DATOS-ES.md`.

---

## 4. CONSENTIMIENTO INFORMADO

**¿Se solicitará consentimiento informado a los participantes?**
☑ **Sí** (adjuntar copia del documento)
☐ No

**Justificación si no se requiere:** — (no aplica)

**Método de obtención del consentimiento:**
☑ **Escrito**
☐ Verbal
☐ Electrónico

*(Si en la práctica se usara firma electrónica institucional, marcar también Electrónico y adjuntar captura del flujo.)*

**Documentos adjuntos:**
- `PARTICIPANT-INFORMATION-SHEET-ES.md`
- `PARTICIPANT-CONSENT-FORM-ES.md`
- Custodia de firmados: `SIGNED-CONSENTS-CUSTODY.md` (firmas fuera de repositorio público)

---

## 5. GESTIÓN DE DATOS Y CONFIDENCIALIDAD

**¿Se recopilarán datos personales o sensibles?**
☑ **Sí** (datos personales en sentido RGPD: trazas de proceso **seudonimizadas** con riesgo residual de reidentificación; **no** categorías especiales del art. 9)
☐ No

**Clarificación para el CEI / DPO:** el estudio **no** recoge categorías especiales (salud, ideología, biometría, vida sexual, origen étnico, etc.) ni encuestas de vida privada. El objeto de interés investigador no es la identidad del alumnado. Las calificaciones e identidades académicas permanecen en sistemas docentes y **fuera** del corpus. Se reconoce honestamente que, bajo RGPD/LOPDGDD, datos seudonimizados pueden seguir siendo datos personales; por ello se aplican medidas de minimización, acceso restringido y no se tratan como «datos anónimos abiertos».

**Medidas de protección de datos:**
Seudonimización (`P01…Pn`); mapa seudónimo↔identidad offline/cifrado y separado; corpus de acceso restringido; sin nube pública de datos de estudiantes; sin publicación de nombres, emails, fotos ni *handles* identificables; extractos publicados solo con consentimiento de difusión; análisis preferente tras cierre de notas (reducción del conflicto docente–investigador); consentimiento y retirada sin efecto académico. Detalle: `PLAN-MANEJO-DATOS-ES.md` y `DATA-MINIMIZATION-STATEMENT.md`.

**Periodo de conservación de los datos:**
Consentimientos: fin del estudio + plazo institucional (propuesta ≥ **5 años** o norma UDIT). Corpus seudonimizado: hasta cierre de publicaciones del ciclo + archivo según política institucional. Mapa seudónimo: destruir cuando deje de ser necesario para retirada/auditoría. Confirmar con DPO (`dpd@udit.es` / `proteccion.datos@udit.es`).

**Método de eliminación de datos al final del estudio:**
☑ **Eliminación digital segura**
☑ **Destrucción de documentos físicos** (si existen consentimientos en papel)
☐ Otro

---

## 6. RIESGOS Y BENEFICIOS DEL ESTUDIO

**¿Existen riesgos para los participantes?**
☐ No
☑ **Sí** (riesgos **bajos / no médicos**, descritos y minimizados)

**Riesgos y minimización:**

| Riesgo | Minimización |
| ------ | ------------ |
| Conflicto docente–investigador (el PI califica) | Consentimiento/custodia preferiblemente independientes; ceguera del docente al consentimiento hasta cerrar notas; retirada sin efecto en la calificación |
| Coerción percibida por jerarquía | Información clara; opt-in; la nota no depende de consentir |
| Reidentificación en PRs/código | Seudonimización; extractos públicos solo con consentimiento de difusión |
| Vigilancia excesiva | Minimización; sin telemetría encubierta de IDE/keystrokes; sin grabación en el diseño mínimo |

**Beneficios esperados:**
Mejora documentada del diseño docente; contribución a la literatura de educación informática sobre aprendizaje auténtico con IA agentica; **ningún** beneficio académico individual por consentir. Beneficio para la comunidad científica: principios de diseño situados transferibles a grupos post-introductorios similares (no inferencia causal poblacional).

---

## 7. CUMPLIMIENTO ÉTICO Y NORMATIVO

**¿El estudio cumple con normativas nacionales e internacionales de ética en investigación?**
☑ **Sí**
☐ No

*(Marco de referencia: principios de integridad investigadora, RGPD / LOPDGDD, buenas prácticas en Computing Education Research, y normativa del CEI-UDIT. Base jurídica propuesta del uso investigador: consentimiento art. 6.1.a RGPD.)*

**¿El estudio ha sido sometido a otro Comité de Ética?**
☑ **No**
☐ Sí

---

## 8. DOCUMENTACIÓN ADJUNTA

| Documento | Estado |
| --------- | ------ |
| ☑ Protocolo de investigación completo | `PROTOCOLO-INVESTIGACION-COMPLETO-ES.md` |
| ☑ Formulario de consentimiento informado | `PARTICIPANT-CONSENT-FORM-ES.md` + hoja de información |
| ☑ Instrumentos de recolección de datos | `INSTRUMENTOS-RECOLECCION-DATOS-ES.md` (sin cuestionario/entrevista) |
| ☑ Autorizaciones institucionales necesarias | `AUTORIZACIONES-INSTITUCIONALES-ES.md` + **adjuntar** acta/correo departamental firmado `[pendiente]` |
| ☑ Plan de manejo de datos y medidas de seguridad | `PLAN-MANEJO-DATOS-ES.md` (+ `DATA-MINIMIZATION-STATEMENT.md`) |
| ☑ Otra documentación relevante | Solicitud narrativa `ETHICS-COMMITTEE-SUBMISSION-ES.md`; Strand A aparada; brief departamental; checklist `CHECKLIST-COMITE-ETICA-ES.md` |

**Especificar otra documentación:**
Declaración de exclusión de Strand A (filosófico, aparado); extracto de guía docente / encargo de la entrega del grupo; diseño detallado EN `STRAND-B-PEDAGOGICAL-DESIGN.md` (referencia).

---

## 9. DECLARACIÓN DEL SOLICITANTE

Declaro que la información proporcionada en este formulario es veraz y que el proyecto será desarrollado cumpliendo los principios éticos y normativos establecidos por el CEI de UDIT. Me comprometo a notificar cualquier modificación al protocolo y a solicitar la evaluación correspondiente en caso de cambios sustanciales.

| Campo | Valor |
| ----- | ----- |
| Firma del solicitante | _______________________________ |
| Fecha | 26 / 09 / 2026 |

---

## INFORMACIÓN EN MATERIA DE PROTECCIÓN DE DATOS PERSONALES

*(Texto institucional del formulario — conservar íntegro en la copia oficial.)*

El responsable del tratamiento de sus datos personales es UDIT ESTUDIOS SUPERIORES INTERNACIONALES, S.L. con NIF B84014265 y domicilio social en Avenida de Alfonso XIII, nº97 – 28016 Madrid (España). […] Contacto: `proteccion.datos@udit.es` · DPD: `dpd@udit.es` · AEPD: https://aepd.es/es

☑ **He leído y acepto el tratamiento de mis datos personales.**

---

## Campos que el solicitante debe completar a mano antes de remitir

1. **n** exacto del grupo / de consentimientos.
2. **Autorización departamental firmada** (adjunto).
3. Firma manuscrita o electrónica en §9.
4. Confirmar con DPO el plazo de conservación si UDIT fija uno distinto de «≥5 años».
5. Si el comité exige custodio independiente: nombre y cargo.
